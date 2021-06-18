from models.elastic.user import UserInDB, Collection, AdminInDB
from models.schemas.user import User, UserRegistrationForm, AdminUser
from models.schemas.jwt import JWTMeta, JWTUser
from models.elastic_models import PaperMetadataCorrectionES, Author
from models.api_models import PaperMetadataCorrection
from passlib.context import CryptContext
from typing import Dict
from datetime import datetime, timedelta
import bcrypt
from services.elastic_service import ElasticService
import requests
import os
import smtplib, ssl
from email.message import EmailMessage
JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
RECAPTCHA_SECRET_KEY = os.environ['RECAPTCHA_SECRET_KEY']
RECAPTCHA_API_ENDPOINT = "https://www.google.com/recaptcha/api/siteverify"
elastic_service = ElasticService()
verification_email_message ="""
Hi %s,


A CiteSeerX account has been automatically generated for you.  To activate this account please visit the following URL:

(If this email is not intented for you, please DO NOT click the link below.)
http://localhost:3000/verify_account/%s

Best,
CiteSeerX
"""
reset_password_email_message ="""
To reset your password please click the following link:

(If this email is not intented for you, please DO NOT click the link below.)
http://localhost:3000/reset_password/%s

Best,
CiteSeerX
"""
class AuthenticationService:        
    
    # Securities
    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()
    
    def verify_password(self, salt: str, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(salt + plain_password, hashed_password)

    def get_password_hash(self, salt, password) -> str:
        return pwd_context.hash(salt + password)

    def is_email_taken(self, email: str) -> bool:
        ''' retrun true if email already taken
        '''
        return self.get_user(email) != None

    def recaptcha(self, token):
        body = { "secret": RECAPTCHA_SECRET_KEY, "response": token}
        res = requests.post(url = RECAPTCHA_API_ENDPOINT, data = body).json()
        return res

    def send_verification_email(self, full_name: str, email: str, token: str):
        msg = EmailMessage()
        email_body = verification_email_message % (full_name, token)
        msg.set_content(email_body)
        msg['Subject'] = f'Please verify your CiteSeerX Account'
        msg['From'] = 'test-csx@ist.psu.edu'
        msg['To'] = email
        context = ssl.create_default_context()
        # Send the message via our own SMTP server.
        s = smtplib.SMTP('smtp.psu.edu')#, 25) 
        s.send_message(msg)
        s.quit()
        return True

    def send_password_reset_email(self, email: str, token: str):
        msg = EmailMessage()
        email_body = reset_password_email_message % (token)
        msg.set_content(email_body)
        msg['Subject'] = f'Reset Password For Your CiteSeerX Account'
        msg['From'] = 'test-csx@ist.psu.edu'
        msg['To'] = email
        context = ssl.create_default_context()
        # Send the message via our own SMTP server.
        s = smtplib.SMTP('smtp.psu.edu', 25) 
        s.send_message(msg)
        s.quit()
        return True

    def activate_account(self, user_in_db):
        try:
            user_in_db.is_activated = True
            user_in_db.save(using=elastic_service.get_connection())
            return True
        except:
            return False
    # Authentication
    def create_user(self, user_data: UserRegistrationForm):
        '''return status
           status:
               0 on success
               -1 on email taken
               -2 db error
        '''
        if self.is_email_taken(user_data.email):
            return -1    
        salt = self.generate_salt()
        hashed_password = self.get_password_hash(salt, user_data.password)
        
        user_in_db = UserInDB(
            salt=salt,
            hashed_password=hashed_password,
            email=user_data.email,
            full_name=user_data.full_name,
            organization=user_data.organization,
            department=user_data.department,
            web_page=user_data.web_page,
            country=user_data.country,
            state=user_data.state,
            monitered_papers=[],
            liked_papers=[],
            is_activated = False
        )
        user_in_db.init(using=elastic_service.get_connection())
        user_in_db.meta.id = user_in_db.email # set email as _id in elasticsearch
        if user_in_db.save(using=elastic_service.get_connection()):
            return 0
        return -2
        
    def create_admin(self, admin_data: AdminUser):
        salt = self.generate_salt()
        hashed_password = self.get_password_hash(salt, admin_data.password)
        
        admin_in_db = AdminInDB(salt=salt,username=admin_data.username, hashed_password=hashed_password)
        admin_in_db.init(using=elastic_service.get_connection())
        admin_in_db.meta.id = admin_in_db.username
        return admin_in_db.save(using=elastic_service.get_connection())

    def authenticate_user(self, email: str, password: str) -> (int, UserInDB):
        '''return (status, UserInDB object)
           status:
               0 on sucess
               -1 on authetication error
               -2 on not activated account
        '''
        user = self.get_user(email)
        if not user or not self.verify_password(user.salt, password, user.hashed_password):
            return -1, None
        if not user.is_activated:
            return -2, None
        return 0, user
    def authenticate_admin(self, username: str, password: str):
        '''return (status, UserInDB object)
           status:
               0 on sucess
               -1 on authetication error
               -2 on not activated account
        '''
        user = AdminInDB.get(id=username, using=elastic_service.get_connection())
        if not user or not self.verify_password(user.salt, password, user.hashed_password):
            return -1, None
        return 0, user


    def get_user(self, email: str) -> UserInDB:
        try:
            return UserInDB.get(id=email, using=elastic_service.get_connection())
        except:
            return None
    def reset_password(self, email, new_password):
        user_in_db = self.get_user(email)
        new_salt = self.generate_salt()
        new_hashed_password = self.get_password_hash(new_salt, new_password)
        return user_in_db.update(salt=new_salt, hashed_password=new_hashed_password, using=elastic_service.get_connection())


    def add_collection_paper(self, user_in_db: UserInDB, pid: str, collection_name: str):
        user_in_db.add_collection_paper(collection_name, pid)
        return user_in_db.save(using=elastic_service.get_connection())
    def delete_collection_paper(self, user_in_db: UserInDB, pid: str, collection_name: str):
        user_in_db.delete_collection_paper(collection_name, pid)
        return user_in_db.save(using=elastic_service.get_connection()) 

    def add_moniter_paper(self, user_in_db: UserInDB, pid):
        if hasattr(user_in_db, 'monitered_papers') and pid not in user_in_db.monitered_papers:
            user_in_db.monitered_papers.append(pid)
        else:
            user_in_db.monitered_papers = [pid]
        return user_in_db.save(using=elastic_service.get_connection())

    def delete_moniter_paper(self, user_in_db: UserInDB, pid):
        if hasattr(user_in_db, 'monitered_papers') and pid in user_in_db.monitered_papers:
            user_in_db.monitered_papers.remove(pid)
            return user_in_db.save(using=elastic_service.get_connection())

    def add_liked_paper(self, user_in_db: UserInDB, pid):
        if hasattr(user_in_db, 'liked_papers') and pid not in user_in_db.liked_papers:
            user_in_db.liked_papers.append(pid)
        else:
            user_in_db.liked_papers = [pid]
        return user_in_db.save(using=elastic_service.get_connection())

    def delete_liked_paper(self, user_in_db: UserInDB, pid):
        if hasattr(user_in_db, 'liked_papers') and pid in user_in_db.liked_papers:
            user_in_db.liked_papers.remove(pid)
            return user_in_db.save(using=elastic_service.get_connection())

    def correct_metadata_request(self, correct_meta: PaperMetadataCorrection, user_email: str):
        correct_meta_ES = PaperMetadataCorrectionES(
            paper_id = correct_meta.id,
            authors = [],
            user_email = user_email,
            title = correct_meta.title,
            abstract = correct_meta.abstract,
            venue = correct_meta.venue,
            venue_type = correct_meta.venue_type,
            year = int(correct_meta.year),
            volume = correct_meta.volume,
            number = correct_meta.number,
            pages = correct_meta.pages,
            publisher = correct_meta.publisher,
            pub_address = correct_meta.pub_address,
            tech_report_num = correct_meta.tech_report_num
        )
        
        for author in correct_meta.authors:

            name_split = author.name.split(" ")
            forename, surname = name_split[0], name_split[-1]    
            correct_meta_ES.authors.append(Author(
                full_name = author.name,
                forename = forename,
                surname = surname,
                affiliation = author.affiliation,
                address = author.address,
                email = author.email)
            )
        correct_meta_ES.save(using=elastic_service.get_connection())
        return

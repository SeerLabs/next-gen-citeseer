from models.elastic.user import UserInDB
from models.schemas.user import User, UserRegistrationForm
from models.schemas.jwt import JWTMeta, JWTUser
from models.elastic_models import PaperMetadataCorrectionES
from models.api_models import PaperMetadataCorrection
from passlib.context import CryptContext
from typing import Dict
from datetime import datetime, timedelta
import jwt
import bcrypt
from services.elastic_service import ElasticService
import requests
import os
JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 3
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
RECAPTCHA_SECRET_KEY = os.environ['RECAPTCHA_SECRET_KEY']
RECAPTCHA_API_ENDPOINT = "https://www.google.com/recaptcha/api/siteverify"
elastic_service = ElasticService()
class AuthenticationService:        
    # JWT
    def create_jwt_token(self, jwt_content: Dict[str, str], secret_key: str, expires_delta: timedelta) ->str:
        to_encode = jwt_content.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).dict())
        return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM).decode()

    def create_user_access_token(self, user: User, secret_key: str) -> str:
        return self.create_jwt_token(
            jwt_content=JWTUser(username=user.username).dict(),
            secret_key=secret_key,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
 
    def get_username_from_token(self, token: str, secret_key: str) -> str:
        try:
            return JWTUser(**jwt.decode(token, secret_key, algorithms=[ALGORITHM])).username
        except jwt.PyJWTError as decode_error:
            raise ValueError("unable to decode JWT token") from decode_error
        except ValidationError as validation_error:
            raise ValueError("malformed payload in token") from validation_error

    # Securities
    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()
    
    def verify_password(self, salt: str, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(salt + plain_password, hashed_password)

    def get_password_hash(self, salt, password) -> str:
        return pwd_context.hash(salt + password)

    def is_username_taken(self, username: str) -> bool:
        return False

    def is_email_taken(self, email: str) -> bool:
        return False
    def recaptcha(self, token):
        body = { "secret": RECAPTCHA_SECRET_KEY, "response": token}
        res = requests.post(url = RECAPTCHA_API_ENDPOINT, data = body)
        return res.json()
    # Authentication
    def create_user(self, user_data: UserRegistrationForm):
        salt = self.generate_salt()
        hashed_password = self.get_password_hash(salt, user_data.password)
        
        user_in_db = UserInDB(
            username=user_data.username,
            salt=salt,
            hashed_password=hashed_password,
            email=user_data.email,
            full_name=user_data.full_name,
            organization=user_data.organization,
            department=user_data.department,
            web_page=user_data.web_page,
            country=user_data.country,
            state=user_data.state,
            collections={},
            monitered_papers=[],
            liked_papers=[]
        )
        user_in_db.meta.id = user_in_db.username # set username is _id in elasticsearch
        # self.fake_users_db[user_in_db.username] = user_in_db.dict()
        return user_in_db.save(using=elastic_service.get_connection())
        
        
    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(user.salt, password, user.hashed_password):
            return False
        return user

    def get_user(self, username: str) -> UserInDB:
        return UserInDB.get(id=username, using=elastic_service.get_connection())

    def change_password(self, username, new_password):
        user_in_db = self.get_user(username)
        new_salt = self.generate_salt()
        new_hashed_password = self.get_password_hash(new_salt, new_password)
        return user_in_db.update(salt=new_salt, hashed_password=new_hashed_password, using=elastic_service.get_connection())


    def collection_add_paper(self, user_in_db: UserInDB, pid: str, collection: str):
        if collection is None:
            collection =  "untitled_collection"
        if hasattr(user_in_db, 'collections') and collection in user_in_db.collections:
            user_in_db.collections[collection].append(pid)
        else:
            user_in_db.collections ={ collection: [pid] }
        return user_in_db.save(using=elastic_service.get_connection())
  
    def add_moniter_paper(self, user_in_db: UserInDB, pid):
        if hasattr(user_in_db, 'monitered_papers') and pid not in user_in_db.monitered_papers:
            user_in_db.monitered_papers.append(pid)
        else:
            user_in_db.monitered_papers = [pid]
        return user_in_db.save(using=elastic_service.get_connection())

    def add_liked_paper(self, user_in_db: UserInDB, pid):
        if hasattr(user_in_db, 'liked_papers') and pid not in user_in_db.liked_papers:
            user_in_db.liked_papers.append(pid)
        else:
            user_in_db.liked_papers = [pid]
        return user_in_db.save(using=elastic_service.get_connection())
    def correct_metadata_request(self, correct_meta: PaperMetadataCorrection, user_in_db: UserInDB):
        correct_meta_ES = PaperMetadataCorrectionES(
            #authors = correct_meta.authors,
            username = user_in_db.username,
            abstract = correct_meta.abstract,
            venue = correct_meta.venue,
            venue_type = correct_meta.venue_type,
            year = int(correct_meta.year),
            volume = correct_meta.volume,
            number = correct_meta.number,
            pages = correct_meta.pages,
            publisher = correct_meta.publisher,
            pub_address = correct_meta.pub_address
            #tech_report_num = correct_meta.tech_report_num
        )
        correct_meta_ES.save(using=elastic_service.get_connection())
        return

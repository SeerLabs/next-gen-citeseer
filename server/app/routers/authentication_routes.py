from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from models.elastic_models import PaperMetadataCorrectionES
from models import elastic_models
from models.elastic.user import UserInDB
from models.schemas.user import User, UserWithToken, UserRegistrationForm, AdminUser
from models.api_models import PaperMetadataCorrection, UserRequest, UserRequestResponse, ProcessRequest
from services.authentication_service import AuthenticationService
from utils.helpers import getKeyOrDefault
from services.elastic_service import ElasticService
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from typing import Optional
import re
from redis import Redis
from datetime import timedelta
elastic_service = ElasticService()
router = APIRouter()
authService = AuthenticationService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "api/login")
SECRET_KEY = ""
email_validate_regex = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

def validate_email(email: str):
    if not re.fullmatch(email_validate_regex, email):
        raise HTTPException(
            status_code=400,
            detail="Invalid Email Address"
        )
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(request, credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    # noinspection PyBroadException
    @staticmethod
    def verify_jwt(request: Request, token: Optional) -> bool:
        is_token_valid: bool = False
        auth_jwt = AuthJWT(request, token)
        try:
            payload = auth_jwt.get_raw_jwt()
        except Exception:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access","refresh"}
    # authjwt_token_location: set = {"cookies"}
    # Only allow JWT cookies to be sent over https
    # authjwt_cookie_secure: bool = False
    # authjwt_cookie_csrf_protect: bool = False
    # authjwt_cookie_samesite: str = 'lax'
    access_expires: int = timedelta(minutes=15)
    refresh_expires: int = timedelta(days=1)

settings = Settings()

@AuthJWT.load_config
def get_config():
    return settings

#redis_conn = Redis(host='localhost', port=6379, db=0, decode_responses=True)
denylist = set()
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in denylist

async def get_current_user(Authorize: AuthJWT = Depends()):#token: str = Depends(oauth2_scheme)):
    Authorize.jwt_required()
    try:
        email = Authorize.get_jwt_subject()#authService.get_email_from_token(token, SECRET_KEY)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or malformed jwt token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_in_db = authService.get_user(email).to_dict()
    if user_in_db:
        return User(
            email=getKeyOrDefault(user_in_db, 'email'),
            full_name=getKeyOrDefault(user_in_db, 'full_name'),
            organization=getKeyOrDefault(user_in_db, 'organization'),
            department=getKeyOrDefault(user_in_db, 'department'),
            web_page=getKeyOrDefault(user_in_db, 'web_page'),
            country=getKeyOrDefault(user_in_db, 'country'),
            state=getKeyOrDefault(user_in_db, 'state'),
            collections=getKeyOrDefault(user_in_db, 'collections', default=[]),
            monitered_papers=getKeyOrDefault(user_in_db, 'monitered_papers', default=[]),
            liked_papers=getKeyOrDefault(user_in_db, 'liked_papers', default=[])
        ) 
    else:
       raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or malformed jwt token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# NOTE: UserInDB contain hashed password, don't ever expose this as response!!
async def get_current_user_in_db(Authorize: AuthJWT = Depends()) -> UserInDB:#token: str = Depends(oauth2_scheme)) -> UserInDB:
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject() #authService.get_email_from_token(token, SECRET_KEY)
    """
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or malformed jwt token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    """
    user_in_db = authService.get_user(email)
    if user_in_db:
        return user_in_db 
    else:
       raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or malformed jwt token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/create_admin")
def register_admin(username: str = Form(...), password: str = Form(...)):
    adminData = AdminUser(username=username,password=password, access_token="")
    is_user_created = authService.create_admin(adminData)
    return {"success": is_user_created }

@router.post("/admin_login")
async def login(username: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):
    auth_status, admin_in_db = authService.authenticate_admin(username, password)
    error_msg = ""
    if auth_status == -1:
        error_msg = "Inccorect email or password"
    if error_msg != "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Authorize.create_access_token(subject="admin")
    
    return AdminUser(username=username, access_token=access_token)


@router.post("/register")
def register(userData: UserRegistrationForm = Depends(UserRegistrationForm.as_form), Authorize: AuthJWT = Depends()):
    validate_email(userData.email)
    is_user_created = authService.create_user(userData)
    token =  Authorize.create_access_token(subject=userData.email) #authService.create_user_access_token(userData.email, SECRET_KEY)
    is_sent = authService.send_verification_email(userData.full_name, userData.email, token) 
    return {"success": is_user_created and is_sent}

@router.post("/activate_account", dependencies=[Depends(JWTBearer())])
def verify_account(UserInDB = Depends(get_current_user_in_db)):
    is_activated = authService.activate_account(UserInDB)
    return { "success": is_activated }

@router.get("/recaptcha")
async def recaptcha(token: str):
    res = authService.recaptcha(token)
    return res

@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):#form_data: OAuth2PasswordRequestForm = Depends()):
    auth_status, user_in_db = authService.authenticate_user(email, password)
    error_msg = ""
    if auth_status == -1:
        error_msg = "Inccorect email or password"
    elif auth_status == -2:
        error_msg = "Account not activated"
    if error_msg != "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = Authorize.create_access_token(subject=email)
    refresh_token = Authorize.create_refresh_token(subject=email)
    # Authorize.set_access_cookies(access_token)
    # Authorize.set_refresh_cookies(refresh_token)
    # token = authService.create_user_access_token(user_in_db.email, SECRET_KEY)
    # refresh_token = authService.create_user_access_token(user_in_db.email, SECRET_KEY)
    user_in_db = user_in_db.to_dict()
    
    return UserWithToken(
        email=getKeyOrDefault(user_in_db, 'email'),
        full_name=getKeyOrDefault(user_in_db, 'full_name'),
        organization=getKeyOrDefault(user_in_db, 'organization'),
        department=getKeyOrDefault(user_in_db, 'department'),
        web_page=getKeyOrDefault(user_in_db, 'web_page'),
        country=getKeyOrDefault(user_in_db, 'country'),
        state=getKeyOrDefault(user_in_db, 'state'),
        collections=getKeyOrDefault(user_in_db, 'collections', default=[]),
        monitered_papers=getKeyOrDefault(user_in_db, 'monitered_papers', default=[]),
        liked_papers=getKeyOrDefault(user_in_db, 'liked_papers', default=[]),
        access_token= access_token,
        refresh_token=refresh_token
    ) 
# Endpoint for revoking the current users access token
@router.delete('/access-revoke', dependencies=[Depends(JWTBearer())])
def access_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    # Store the tokens in redis with the value true for revoked.
    # We can also set an expires time on these tokens in redis,
    # so they will get automatically removed after they expired.
    jti = Authorize.get_raw_jwt()['jti']
    #redis_conn.setex(jti,settings.access_expires,'true')
    denylist.add(jti)
    return {"detail":"Access token has been revoke"}

# Endpoint for revoking the current users refresh token
@router.delete('/refresh-revoke', dependencies=[Depends(JWTBearer())])
def refresh_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    jti = Authorize.get_raw_jwt()['jti']
    #redis_conn.setex(jti,settings.refresh_expires,'true')
    denylist.add(jti)
    return {"detail":"Refresh token has been revoke"}

@router.post("/refresh_token", dependencies=[Depends(JWTBearer())])
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    new_refresh_token = Authorize.create_refresh_token(subject=current_user)
    denylist.add(Authorize.get_raw_jwt()['jti'])
    return { "access_token": new_access_token, "refresh_token": new_refresh_token}


@router.get("/user_profile", dependencies=[Depends(JWTBearer())])
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/password_reset_email")
async def password_reset_email(email: str = Form(...) , Authorize: AuthJWT = Depends()):
    validate_email(email)
    token =  Authorize.create_access_token(subject=email)#authService.create_user_access_token(email, SECRET_KEY)
    authService.send_password_reset_email(email, token)
    return {"success": True} 

@router.post("/reset_password", dependencies=[Depends(JWTBearer())])
async def loged_in_reset_password(new_password: str = Form(...), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    email = Authorize.get_jwt_subject()# authService.get_email_from_token(token, SECRET_KEY)
    authService.reset_password(email, new_password)
    return "success"

@router.put("/collection/name", dependencies=[Depends(JWTBearer())])
async def create_collection(collection_name: str = None, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.create_collection(collection_name)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="Collection already exist",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}

@router.put("/collection/rename", dependencies=[Depends(JWTBearer())])
async def rename_collection(collection_name, new_collection_name, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.rename_collection(collection_name, new_collection_name)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="collection_name not found",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}

@router.delete("/collection/name", dependencies=[Depends(JWTBearer())])
async def delete_collection(collection_name: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.delete_collection(collection_name)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="collection_name not found",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}


@router.put("/collection/paper", dependencies=[Depends(JWTBearer())])
async def add_collection_paper(pid: str, collection_name: str = None, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.add_collection_paper(collection_name, pid)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="collection_name not found or pid already in collection",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}
@router.delete("/collection/paper", dependencies=[Depends(JWTBearer())])
async def delete_collection_paper(pid: str, collection_name: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.delete_collection_paper(collection_name, pid)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="collection_name not found or pid not found",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}

@router.put("/moniter_paper/{pid}", dependencies=[Depends(JWTBearer())])
async def add_moniter_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.add_moniter_paper(user_in_db, pid)
    return {"success": True}

@router.delete("/moniter_paper/{pid}", dependencies=[Depends(JWTBearer())])
async def delete_moniter_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.delete_moniter_paper(user_in_db, pid)
    return {"success": True}

@router.put("/liked_paper/{pid}", dependencies=[Depends(JWTBearer())])

async def add_liked_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.add_liked_paper(user_in_db, pid)
    return {"success": True}

@router.delete("/liked_paper/{pid}", dependencies=[Depends(JWTBearer())])
async def delete_liked_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.delete_liked_paper(user_in_db, pid)
    return { "success": True }

@router.post("/correct_metadata", dependencies=[Depends(JWTBearer())])
async def correct_metadata_request(correct_meta: PaperMetadataCorrection, Authorize: AuthJWT = Depends()):#token = Depends(oauth2_scheme)):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject() #authService.get_email_from_token(token, SECRET_KEY)
    authService.correct_metadata_request(correct_meta, user_email)
    return {"success": True}

@router.get("/get_correct_metadatas")#, dependencies=[Depends(JWTBearer())])
def get_correct_metadata_request():
    #Authorize.jwt_required()
    #user = Authorize.get_jwt_subject()
    results = PaperMetadataCorrectionES.search(using=elastic_service.get_connection()).execute()
    response = []
    for doc in results:#['hits']['hits']:
        doc = vars(doc)["_d_"]
        authors = []
        #for author in doc["authors"]:
        #    authors.append(author)
        #doc["authors"] = authors
        response.append(doc)
    return response

@router.delete('/unlist/{id}')
def unlist_paper(id: str):
    # Get Cluster for paper
    search_cluster = elastic_models.Cluster.search(using=elastic_service.get_connection())
    search_cluster = search_cluster.filter('term', paper_id=id)
    response = search_cluster.execute()
    cluster_id = response['hits']['hits'][0]['_id']

    # Make PDF availability as False
    cluster = elastic_models.Cluster.get(id=cluster_id, using=elastic_service.get_connection())
    cluster.has_pdf = False
    cluster.save(using=elastic_service.get_connection())

    # Create an Audit entry
    new_user_request = elastic_models.UserRequest()
    new_user_request.request_type = "UNLIST"
    new_user_request.paper_id = id
    new_user_request.status = "DONE"
    new_user_request.save(using=elastic_service.get_connection())


@router.post('/edit/new', dependencies=[Depends(JWTBearer())])
def unlist_paper(edit_request: UserRequest, Authorize: AuthJWT = Depends()):
    # Create an Audit entry
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    
    pub_info = elastic_models.PubInfo()
    pub_info.date = edit_request.publish_date
    pub_info.meeting = edit_request.meeting
    pub_info.publisher = edit_request.publisher
    
    author_list = []
    for author in edit_request.authors:
        new_author = elastic_models.Author()
        new_author.fullname = author.name
        new_author.affiliation = author.affiliation
        new_author.address = author.address
        new_author.email = author.email
        author_list.append(new_author)

    new_user_request = elastic_models.UserRequest()
    new_user_request.request_type = "EDIT"
    new_user_request.paper_id = edit_request.paper_id
    new_user_request.requester_email = user_email 
    new_user_request.reason_or_details = edit_request.reason_or_details
    new_user_request.title = edit_request.title
    new_user_request.abstract = edit_request.abstract
    new_user_request.authors = author_list
    new_user_request.pub_info = pub_info
    new_user_request.status = "PENDING"
    new_user_request.save(using=elastic_service.get_connection())
    return {"success": True}

@router.get('/edit/get_pending', dependencies=[Depends(JWTBearer())])
def unlist_paper(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    
    search_request = elastic_models.UserRequest.search(using=elastic_service.get_connection())
    search_request = search_request.filter("term", request_type = "EDIT")
    search_request = search_request.filter("term", status = "PENDING")
    result = search_request.execute()
    response = []
    for hit in result:
        #req = UserRequestResponse(request_id = hit.meta.id, user_request = hit.to_dict())
        req = {"request_id": hit.meta.id, "user_request": hit.to_dict()}
        response.append(req)

    return response

@router.get('/edit/get_archived', dependencies=[Depends(JWTBearer())])
def unlist_paper(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    
    search_request = elastic_models.UserRequest.search(using=elastic_service.get_connection())
    search_request = search_request.filter("term", request_type = "EDIT")
    search_request = search_request.filter("terms", status = ["COMMITTED", "DENIED", "MODIFIED"])
    result = search_request.execute()
    response = []
    for hit in result:
        #req = UserRequestResponse(request_id = hit.meta.id, user_request = hit.to_dict())
        req = {"request_id": hit.meta.id, "user_request": hit.to_dict()}
        response.append(req)
    
    return response


@router.get('/edit/init')
def unlist_paper():
    request = elastic_models.UserRequest()
   
    request.init(using=elastic_service.get_connection())
    return {"success": True}


@router.post('/edit/commit', dependencies=[Depends(JWTBearer())])
def unlist_paper(req: ProcessRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    
    user_request = elastic_models.UserRequest.get(id=req.request_id, using=elastic_service.get_connection())

    if user_request.request_type != "EDIT":
        return {"success": False, "message": "not an EDIT request"}
   
    user_request.status = "COMMITTED"
    user_request.reviewer_comment = req.reviewer_comment
    user_request.save(using=elastic_service.get_connection())
    return {"success": True}

@router.post('/edit/deny', dependencies=[Depends(JWTBearer())])
def unlist_paper(req: ProcessRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_email = Authorize.get_jwt_subject()
    
    user_request = elastic_models.UserRequest.get(id=req.request_id, using=elastic_service.get_connection())

    if user_request.request_type != "EDIT":
        return {"success": False, "message": "not an EDIT request"}
   
    user_request.status = "DENIED"
    user_request.reviewer_comment = req.reviewer_comment
    user_request.save(using=elastic_service.get_connection())
    return {"success": True}


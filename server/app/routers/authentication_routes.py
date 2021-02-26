from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from models.elastic.user import UserInDB
from models.schemas.user import User, UserWithToken, UserRegistrationForm
from models.api_models import PaperMetadataCorrection
from services.authentication_service import AuthenticationService
from utils.helpers import getKeyOrDefault
from services.elastic_service import ElasticService
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from typing import Optional
import re
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
settings = Settings()
@AuthJWT.load_config
def get_config():
    return settings

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


@router.post("/register")
def register(userData: UserRegistrationForm = Depends(UserRegistrationForm.as_form), Authorize: AuthJWT = Depends()):
    validate_email(userData.email)
    is_user_created = authService.create_user(userData)
    print(userData.email)
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
    return reis

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

@router.post("/refresh_token", dependencies=[Depends(JWTBearer())])
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return { "access_token": new_access_token}


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

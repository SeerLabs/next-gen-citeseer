from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.elastic.user import UserInDB
from models.schemas.user import User, UserWithToken, UserRegistrationForm
from models.api_models import PaperMetadataCorrection
from services.authentication_service import AuthenticationService
from utils.helpers import getKeyOrDefault
from services.elastic_service import ElasticService
elastic_service = ElasticService()
router = APIRouter()
authService = AuthenticationService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "api/login")

SECRET_KEY = ""

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        email = authService.get_email_from_token(token, SECRET_KEY)
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


# NOTE: UserInDB contain hashed password, don't ever return this to user!!
async def get_current_user_in_db(token: str = Depends(oauth2_scheme)) -> UserInDB:
    try:
        email = authService.get_email_from_token(token, SECRET_KEY)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or malformed jwt token",
            headers={"WWW-Authenticate": "Bearer"},
        )
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
def register(userData: UserRegistrationForm):
    is_user_created = authService.create_user(userData)
    token = authService.create_user_access_token(userData.email, SECRET_KEY)
    status = authService.send_verification_email(userData.full_name, userData.email, token) 
    if is_user_created: 
        return "success"
    else:
        return "failed"

@router.post("/activate_account")
def verify_account(token: str):
    status = authService.activate_account(token, SECRET_KEY)
    return { "success": status }

@router.get("/recaptcha")
async def recaptcha(token: str):
    res = authService.recaptcha(token)
    return res

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_status, user_in_db = authService.authenticate_user(form_data.username, form_data.password)
    error_msg = ""
    if auth_status == -1:
        error_msg = "Inccorect username or password"
    elif auth_status == -2:
        error_msg = "Account not activated"
    if error_msg != "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authService.create_user_access_token(user_in_db.email, SECRET_KEY)
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
        access_token=token
    ) 


@router.get("/user_profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/password_reset_email")
async def password_reset_email(email: str):
    token = authService.create_user_access_token(email, SECRET_KEY)
    authService.send_password_reset_email(email, token)
    return "success" 

@router.post("/reset_password")
async def loged_in_reset_password(new_password, token: str):
    email = authService.get_email_from_token(token, SECRET_KEY)
    authService.reset_password(email, new_password)
    return "success"

@router.put("/collection/name")
async def create_collection(collection_name: str = None, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.create_collection(collection_name)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="Collection already exist",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}

@router.put("/collection/rename")
async def rename_collection(collection_name, new_collection_name, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.rename_collection(collection_name, new_collection_name)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="collection_name not found",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}

@router.delete("/collection/name")
async def delete_collection(collection_name: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.delete_collection(collection_name)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="collection_name not found",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}


@router.put("/collection/paper")
async def add_collection_paper(pid: str, collection_name: str = None, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.add_collection_paper(collection_name, pid)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="collection_name not found or pid already in collection",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}
@router.delete("/collection/paper")
async def delete_collection_paper(pid: str, collection_name: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    res_status = user_in_db.delete_collection_paper(collection_name, pid)    
    if res_status == -1:
        raise HTTPException(
            status_code=404,
            detail="collection_name not found or pid not found",
        )

    user_in_db.save(using=elastic_service.get_connection())
    return {"success": True}

@router.put("/moniter_paper/{pid}")
async def add_moniter_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.add_moniter_paper(user_in_db, pid)
    return "success"

@router.delete("/moniter_paper/{pid}")
async def delete_moniter_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.delete_moniter_paper(user_in_db, pid)
    return "success"

@router.put("/liked_paper/{pid}")
async def add_liked_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.add_liked_paper(user_in_db, pid)
    return "success"

@router.delete("/liked_paper/{pid}")
async def delete_liked_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.delete_liked_paper(user_in_db, pid)
    return "success"

@router.put("/correct_metadata")
async def correct_metadata_request(correct_meta: PaperMetadataCorrection, token = Depends(oauth2_scheme)):
    user_email = authService.get_email_from_token(token, SECRET_KEY)
    authService.correct_metadata_request(correct_meta, user_email)
    return "success"

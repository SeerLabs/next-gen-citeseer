from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.elastic.user import UserInDB
from models.schemas.user import User, UserWithToken, UserRegistrationForm
from models.api_models import PaperMetadataCorrection
from services.authentication_service import AuthenticationService
from utils.helpers import getKeyOrDefault
router = APIRouter()
authService = AuthenticationService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "api/login")

SECRET_KEY = ""

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        username = authService.get_username_from_token(token, SECRET_KEY)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or malformed jwt token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_in_db = authService.get_user(username).to_dict()
    if user_in_db:
        return User(
            username=getKeyOrDefault(user_in_db, 'username'),
            email=getKeyOrDefault(user_in_db, 'email'),
            full_name=getKeyOrDefault(user_in_db, 'full_name'),
            organization=getKeyOrDefault(user_in_db, 'organization'),
            department=getKeyOrDefault(user_in_db, 'department'),
            web_page=getKeyOrDefault(user_in_db, 'web_page'),
            country=getKeyOrDefault(user_in_db, 'country'),
            state=getKeyOrDefault(user_in_db, 'state'),
            collections=getKeyOrDefault(user_in_db, 'collections', default={}),
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
        username = authService.get_username_from_token(token, SECRET_KEY)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or malformed jwt token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_in_db = authService.get_user(username)
    if user_in_db:
        return user_in_db 
    else:
       raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or malformed jwt token",
            headers={"WWW-Authenticate": "Bearer"},
        )



@router.post("/register")
async def register(userData: UserRegistrationForm):
    is_user_created = authService.create_user(userData)
    if is_user_created:
        return "success"
    else:
        return "failed"


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_in_db = authService.authenticate_user(form_data.username, form_data.password)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    token = authService.create_user_access_token(user_in_db, SECRET_KEY)
    user_in_db = user_in_db.to_dict()
    
    return UserWithToken(
        username=getKeyOrDefault(user_in_db, 'username'),
        email=getKeyOrDefault(user_in_db, 'email'),
        full_name=getKeyOrDefault(user_in_db, 'full_name'),
        organization=getKeyOrDefault(user_in_db, 'organization'),
        department=getKeyOrDefault(user_in_db, 'department'),
        web_page=getKeyOrDefault(user_in_db, 'web_page'),
        country=getKeyOrDefault(user_in_db, 'country'),
        state=getKeyOrDefault(user_in_db, 'state'),
        collections=getKeyOrDefault(user_in_db, 'collections', default={}),
        monitered_papers=getKeyOrDefault(user_in_db, 'monitered_papers', default=[]),
        liked_papers=getKeyOrDefault(user_in_db, 'liked_papers', default=[]),
        access_token=token
    ) 


@router.get("/user_profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/change_password")
async def change_password(new_password, user: User = Depends(get_current_user)):
    authService.change_password(user.username, new_password)
    return "success"


@router.post("/collection")
async def collection_add_paper(pid: str, collection: str = None, user_in_db: UserInDB = Depends(get_current_user_in_db)):
     authService.collection_add_paper(user_in_db, pid, collection)
     return "success"


@router.post("/moniter_paper/{pid}")
async def add_moniter_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.add_moniter_paper(user_in_db, pid)
    return "success"


@router.post("/liked_paper/{pid}")
async def add_liked_paper(pid: str, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.add_liked_paper(user_in_db, pid)
    return "success"


@router.post("/correct_metadata")
async def correct_metadata_request(correct_meta: PaperMetadataCorrection, user_in_db: UserInDB = Depends(get_current_user_in_db)):
    authService.correct_metadata_request(correct_meta, user_in_db)
    return "success"

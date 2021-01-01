from pydantic import BaseModel, typing
from typing import List, Optional, Dict

class User(BaseModel):
    email: str
    full_name: str
    organization: str
    department: str
    web_page: str
    country: str
    state: str
    collections: List[Dict]
    monitered_papers:List[str]
    liked_papers: List[str]

class UserWithToken(User):
    access_token: str

class UserRegistrationForm(BaseModel):
    password: str
    email: str
    full_name: str
    organization: str
    department: str
    web_page: str
    country: str
    state: str
    

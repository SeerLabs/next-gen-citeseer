from pydantic import BaseModel, typing
from typing import List, Optional, Dict
from fastapi import Form

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
    refresh_token: str

class AdminUser(BaseModel):
    username: str
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
    @classmethod
    def as_form(
        cls,
        password: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(...),
        organization: str = Form(""),
        department: str = Form(""),
        web_page: str = Form(""),
        country: str = Form(""),
        state: str = Form("")
    ):
        return cls(
            password = password,
            email = email,
            full_name = full_name,
            organization = organization,
            department = department,
            web_page = web_page,
            country = country,
            state = state
        )
    

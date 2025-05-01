from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str

class Post(BaseModel):
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)

    
class UserCreate(BaseModel):
    email: EmailStr  # automatically checks if its a valid email or not
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    date_joined: datetime

    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
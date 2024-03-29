from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    publish: str

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
class Post(PostBase):
    id: int
    created_at: datetime
    ower_id: int
    onwer: UserOut

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: int        

class TokenData(BaseModel):
    id: Optional[str] = None
    token_type: str

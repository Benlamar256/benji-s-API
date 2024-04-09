from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    Full_name: str
    test_date: str
    Age:int
    Dosage: str
    sex: str


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    Full_Name: str
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
    Full_Name: str
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
    token_type: str     

class TokenData(BaseModel):
    id: Optional[str] = None
    token_type: str

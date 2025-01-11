from pydantic import BaseModel
from typing import Literal
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    hashed_password: str
    name: str
    age: int
    gender: Literal["male", "female", "other"]
    

class UserInfoResponse(BaseModel):
    name: str
    age: int
    gender: str

    class Config:
        from_attributes = True
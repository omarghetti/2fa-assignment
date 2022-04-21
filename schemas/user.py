from typing import Optional
from pydantic import BaseModel


class UserToken(BaseModel):
    access_token: str
    expires_on: str


class UserBase(BaseModel):
    email: str
    enable_2fa: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str
    otp_secret: Optional[str]

    class Config:
        orm_mode = True

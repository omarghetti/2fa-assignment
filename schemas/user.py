from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    enable_2fa: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True

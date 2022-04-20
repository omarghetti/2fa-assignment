from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    enable2fa: bool

import email
from schemas.user import UserCreate
from sqlalchemy.orm import Session
from security import pwd_context
from models.user import User


async def register_user(user: UserCreate, db: Session):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        enable_2fa=user.enable_2fa
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

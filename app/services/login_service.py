from datetime import datetime, timedelta
from app.schemas.user import UserCreate, UserToken
from sqlalchemy.orm import Session
from app.security import pwd_context
from app.models.user import LoginSession, User
import secrets
import pyotp
import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"


async def register_user(user: UserCreate, db: Session):
    hashed_password = pwd_context.hash(user.password)
    otp_secret = pyotp.random_base32() if user.enable_2fa else None
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        otp_secret=otp_secret,
        enable_2fa=user.enable_2fa
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def authenticate_user(username: str, password: str, db: Session):
    user = await get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_session_token(user: User):
    encoded_jwt = jwt.encode({"data": user.email}, SECRET_KEY, ALGORITHM)
    user_token = UserToken(access_token=encoded_jwt,
                           expires_on=(datetime.utcnow() + timedelta(hours=1)).strftime("%m/%d/%Y, %H:%M:%S"))
    return user_token


async def store_login_attempt(user: User, db: Session):
    totp = pyotp.totp.TOTP(user.otp_secret).now()
    db_session = LoginSession(
        identifier=create_session_identifier(), otp_code=totp, user_id=user.id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    print(totp)
    return db_session


async def verify_otp(code: str, email: str, db: Session):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    otp_code = db.query(LoginSession).filter(
        LoginSession.user_id == user.id).first()
    session_token = await create_session_token(user)
    return session_token


async def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


async def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def create_session_identifier():
    return secrets.token_hex(16)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

from fastapi import FastAPI, Depends, HTTPException, status
from app.schemas.user import OtpVerifyPayload, User, UserCreate
from app.services.login_service import authenticate_user, register_user, create_session_token, store_login_attempt, verify_otp
from app.services.database_service import create_database, get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

app = FastAPI()

create_database()


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="username non valido"
        )
    if not user.enable_2fa:
        access_token = await create_session_token(user)
        return {"access_token": access_token.access_token, "expires_on": access_token.expires_on}
    await store_login_attempt(user, db)
    return {"message": "login attempt waiting for otp verification"}


@app.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    registered_user = await register_user(user, db)
    return registered_user


@app.post("/verify")
async def verifyOtp(otpPayload: OtpVerifyPayload, db: Session = Depends(get_db)):
    otp_verified = await verify_otp(otpPayload.code, otpPayload.email, db)
    if not otp_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="OTP non valido"
        )
    return {"access_token": otp_verified.access_token, "expires_on": otp_verified.expires_on}

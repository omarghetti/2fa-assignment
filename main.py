from fastapi import FastAPI, Depends
from schemas.user import User, UserCreate
from services.login_service import register_user
from services.database_service import create_database, get_db
from sqlalchemy.orm import Session

app = FastAPI()

create_database()


@app.get("/login")
async def login():
    return {"message": "User Logged In"}


@app.post("/register", response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    registered_user = await register_user(user, db)
    return registered_user


@app.get("/verify")
async def verifyOtp():
    return {"message": "OTP Correct"}

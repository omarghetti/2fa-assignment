from fastapi import FastAPI
from models.user import User

app = FastAPI()


@app.get("/login")
async def login():
    return {"message": "User Logged In"}


@app.post("/register")
async def register(user: User):
    return {"message": "User Registered", "UserName": user.username, "enabled2fa": user.enable2fa}


@app.get("/verify")
async def verifyOtp():
    return {"message": "OTP Correct"}

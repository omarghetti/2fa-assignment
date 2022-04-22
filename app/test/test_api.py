from datetime import datetime, timedelta
import app.test.db as _db
from app.main import app
from app.db.db import Base
from app.services.database_service import get_db
from httpx import AsyncClient
import pytest

app.dependency_overrides[get_db] = _db.get_test_db

client = AsyncClient(app=app, base_url="http://test")

Base.metadata.create_all(bind=_db.db_engine)


@pytest.mark.asyncio
async def test_register_new_user_disabled():
    disabled_request = {"email": "test_disabled@gmail.com",
                        "enable_2fa": False, "password": "ciao1234"}
    response = await client.post("/register", json=disabled_request)
    data = response.json()
    otp_secret = data["otp_secret"]

    assert response.status_code == 200
    assert otp_secret == None


@pytest.mark.asyncio
async def test_register_new_user_enabled():
    enabled_request = {"email": "test_enabled@gmail.com",
                       "enable_2fa": True, "password": "ciao1234"}
    response = await client.post("/register", json=enabled_request)
    data = response.json()
    otp_secret = data["otp_secret"]

    assert response.status_code == 200
    assert len(otp_secret) == 32


@pytest.mark.asyncio
async def test_login_failed():
    login_request = {"username": "test_disabled@gmail.com",
                     "password": "ciao1234"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await client.post("/login", data=login_request, headers=headers)

    assert response.status_code == 401

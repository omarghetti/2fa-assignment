from app.main import app
from httpx import AsyncClient
import pytest

client = AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_register_new_user_disabled(get_test_db):
    disabled_request = {"email": "test_disabled@gmail.com",
                        "enable_2fa": False, "password": "ciao1234"}
    response = await client.post("/register", json=disabled_request)
    data = response.json()
    otp_secret = data["otp_secret"]

    assert response.status_code == 200
    assert otp_secret == None


@pytest.mark.asyncio
async def test_register_new_user_enabled(get_test_db):
    enabled_request = {"email": "test_enabled@gmail.com",
                       "enable_2fa": True, "password": "ciao1234"}
    response = await client.post("/register", json=enabled_request)
    data = response.json()
    otp_secret = data["otp_secret"]

    assert response.status_code == 200
    assert len(otp_secret) == 32


@pytest.mark.asyncio
async def test_login_failed(get_test_db):
    login_request = {"username": "test_disabled@gmail.com",
                     "password": "ciao1234"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await client.post("/login", data=login_request, headers=headers)

    assert response.status_code == 401

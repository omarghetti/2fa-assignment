from itsdangerous import json
from app.main import app
from httpx import AsyncClient
import pytest
from app.schemas.user import UserCreate
from app.services.login_service import register_user, store_login_attempt

client = AsyncClient(app=app, base_url="http://test")


@pytest.fixture
async def create_registered_user_disabled_2fa(get_test_db):
    yield await register_user(UserCreate(email="test.disabled@gmail.com", enable_2fa=False,
                                         password="ciao1234"), get_test_db)


@pytest.fixture
async def create_registered_user_enabled_2fa(get_test_db):
    yield await register_user(UserCreate(email="test.enabled@gmail.com", enable_2fa=True,
                                         password="ciao1234"), get_test_db)


@pytest.fixture
async def create_login_attempt_successful(create_registered_user_enabled_2fa, get_test_db):
    yield await store_login_attempt(create_registered_user_enabled_2fa, get_test_db)


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


@pytest.mark.asyncio
async def test_login_successful(create_registered_user_disabled_2fa, async_client):
    login_request = {"username": "test.disabled@gmail.com",
                     "password": "ciao1234"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = await async_client.post("/login", data=login_request, headers=headers)

    assert response.status_code == 200
    assert response.json()["access_token"] is not None


@pytest.mark.asyncio
async def test_validate_otp_successful(async_client, create_login_attempt_successful):
    validation_request = {
        "code": create_login_attempt_successful.otp_code, "email": "test.enabled@gmail.com"}

    response = await async_client.post("/verify", json=validation_request)

    assert response.status_code == 200
    assert response.json()["access_token"] is not None

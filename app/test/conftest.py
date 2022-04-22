from httpx import AsyncClient
import pytest
import sqlalchemy as _sql
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from app.db.db import Base, SessionLocal
from app.services.database_service import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"


@pytest.fixture(scope="session")
def db_engine():
    engine = _sql.create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def get_test_db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    db = SessionLocal(bind=connection)
    app.dependency_overrides[get_db] = lambda: db
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
async def async_client(get_test_db):
    app.dependency_overrides[get_db] = lambda: get_test_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

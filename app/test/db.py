import pytest
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"

db_engine = _sql.create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                               "check_same_thread": False})

TestSessionLocal = _orm.sessionmaker(
    autocommit=False, autoflush=False, bind=db_engine)


def get_test_db():
    connection = db_engine.connect()
    transaction = connection.begin()
    db = TestSessionLocal(bind=connection)
    yield db
    db.rollback()
    connection.close()

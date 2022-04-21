import db.db as _db


def create_database():
    return _db.Base.metadata.create_all(bind=_db.db_engine)


def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

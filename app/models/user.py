from enum import unique
import sqlalchemy as _sql
from sqlalchemy.orm import relationship
import db.db as _database


class User(_database.Base):
    __tablename__ = "user"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    otp_secret = _sql.Column(_sql.String)
    enable_2fa = _sql.Column(_sql.Boolean, default=False)
    login_sessions = relationship("LoginSession")


class LoginSession(_database.Base):
    __tablename__ = "loginsession"
    id = _sql.Column(_sql.Integer, primary_key=True)
    identifier = _sql.Column(_sql.String, unique=True, index=True)
    otp_code = _sql.Column(_sql.String)
    user_id = _sql.Column(
        _sql.Integer, _sql.ForeignKey("user.id"), nullable=False)

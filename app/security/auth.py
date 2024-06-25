from datetime import timedelta, timezone, datetime

import jwt
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from settings import get_settings

settings = get_settings()


def create_access_token(data: dict, expires_time: datetime | None = None):
    to_encode = data.copy()
    if expires_time:
        expire = expires_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def create_session(session_key, user_id, expire_datetime):
    db_session: Session = next(get_db())
    try:
        session_instance = models.Session(
            user_id=user_id,
            expire_datetime=expire_datetime,
            session_key=session_key
        )
        db_session.add(session_instance)
        db_session.commit()
    finally:
        db_session.close()


def revoke_session(session_key):
    db_session: Session = next(get_db())
    try:
        session_q = db_session.query(models.Session).filter_by(
            session_key=session_key
        )
        session_q.delete()
        db_session.commit()
    finally:
        db_session.close()

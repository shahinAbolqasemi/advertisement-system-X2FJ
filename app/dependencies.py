import uuid
from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import Token
from app.security.auth import create_access_token, create_session, revoke_session
from settings import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(request: Request, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not request.user.is_authenticated:
        raise credentials_exception

    return request.user.dict()


async def authenticate_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db_session: Annotated[Session, Depends(get_db)]
) -> Token:
    user = db_session.query(User).filter_by(username=form_data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username or password is wrong.",
        )
    access_token_expires_time = datetime.now(timezone.utc) + \
                                timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    session_key = uuid.uuid4().hex
    access_token = create_access_token(
        data={"sub": user.email, 'session_key': session_key}, expires_time=access_token_expires_time
    )
    create_session(session_key, user.id, access_token_expires_time)

    return Token(access_token=access_token, token_type='bearer')

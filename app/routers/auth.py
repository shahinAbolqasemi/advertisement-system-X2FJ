from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import constants, schemas
from .. import models
from ..dependencies import authenticate_user, get_db, get_current_user
from ..schemas import UserCreate, User
from ..schemas.base import StandardResponse, ResponseStatus
from ..security.auth import revoke_session
from ..security.password import get_password_hash

router = APIRouter(
    prefix='',
    tags=['authentication']
)


@router.post(
    '/login',
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK
)
async def login(token: Annotated[schemas.Token, Depends(authenticate_user)]):
    return token


@router.post('/logout')
async def logout(user: Annotated[dict, Depends(get_current_user)]):
    revoke_session(user['session_key'])
    return StandardResponse(status=ResponseStatus.SUCCESS)


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db_session: Annotated[Session, Depends(get_db)]):
    user_instance = models.User(
        username=user.email,
        email=user.email,
        firstname=user.firstname,
        lastname=user.lastname,
        hashed_password=get_password_hash(user.password)
    )
    db_session.add(user_instance)
    db_session.commit()
    db_session.refresh(user_instance)

    return StandardResponse(
        status=ResponseStatus.SUCCESS,
        message=constants.ROUTER_AUTH_LOGIN_SUCCESS,
        data=User.model_validate(user_instance).model_dump()
    )

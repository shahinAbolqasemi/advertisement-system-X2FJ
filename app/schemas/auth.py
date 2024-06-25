from datetime import datetime

from pydantic import BaseModel

from app.schemas.user import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    session_key: str | None = None


class Session(BaseModel):
    id: int
    user_id: int
    expire_datetime: datetime
    session_key: str
    revoked: bool


class UserAuthBase(User):
    session_key: str | None = None

    def is_authenticated(self) -> bool:
        return self.id is not None


class AuthenticatedUser(UserAuthBase):
    pass


class AnonymousUser(UserAuthBase):
    id: int | None = None
    username: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    hashed_password: str | None = None

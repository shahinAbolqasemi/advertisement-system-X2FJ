import typing

import jwt
from jose import JWTError
from jwt import ExpiredSignatureError
from starlette import status
from starlette.authentication import AuthenticationBackend, AuthenticationError, AuthCredentials, UnauthenticatedUser
from starlette.requests import HTTPConnection
from starlette.responses import Response, PlainTextResponse
from starlette.types import Receive, Send, Scope, ASGIApp

from app.schemas.auth import TokenData
from settings import get_settings
from .models.user import User
from .schemas.auth import AuthenticatedUser, AnonymousUser

settings = get_settings()


class BearerTokenAuthBackend(AuthenticationBackend):
    """
    This is a custom auth backend class that will allow you to authenticate your request and return auth and user as
    a tuple
    """

    def __init__(self, app) -> None:
        self.app = app
        super().__init__()

    async def authenticate(self, request):
        # This function is inherited from the base class and called by some other class

        auth = request.headers.get("Authorization")
        if auth is not None:
            try:
                scheme, token = auth.split()
                if scheme.lower() != 'bearer':
                    return auth, AnonymousUser()
                decoded = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"]
                )
            except (ValueError, UnicodeDecodeError, JWTError) as exc:
                raise AuthenticationError('Invalid JWT Token.')
            except ExpiredSignatureError:
                raise AuthenticationError('Signature has expired')
            db = next(self.app.state.db)
            try:
                username: str = decoded.get("sub")
                session_key: str = decoded.get("session_key")
                token_data = TokenData(username=username, session_key=session_key)
                user_in_db = db.query(User).filter_by(username=token_data.username).first()
            finally:
                db.close()

            if not user_in_db:
                return auth, AnonymousUser()
        else:
            return auth, AnonymousUser()
        # This is little hack rather making a generator function for get_db
        user = AuthenticatedUser.model_validate(user_in_db)
        user.session_key = session_key
        return auth, user


class AuthenticationMiddleware:
    def __init__(
            self,
            app: ASGIApp,
            backend: AuthenticationBackend,
            on_error: typing.Optional[
                typing.Callable[[HTTPConnection, AuthenticationError], Response]
            ] = None,
    ) -> None:
        self.app = app
        self.backend = backend
        self.on_error: typing.Callable[
            [HTTPConnection, AuthenticationError], Response
        ] = on_error if on_error is not None else self.default_on_error

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)

        try:
            auth_result = await self.backend.authenticate(conn)
        except AuthenticationError as exc:
            response = self.on_error(conn, exc)
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1000})
            else:
                await response(scope, receive, send)
            return

        if auth_result is None:
            auth_result = AuthCredentials(), UnauthenticatedUser()
        scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)

    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception) -> Response:
        if isinstance(exc, AuthenticationError):
            return PlainTextResponse(str(exc), status_code=status.HTTP_401_UNAUTHORIZED)
        return PlainTextResponse(str(exc), status_code=400)

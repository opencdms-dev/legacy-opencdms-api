from typing import Optional
from fastapi.exceptions import HTTPException

from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from jose.exceptions import JWTError
from starlette.types import Scope, Receive, Send, ASGIApp
from jose import jwt
from apps.auth.services import user_service
from config import app_config
from apps.auth.db.engine import SessionLocal
from apps.auth.db.models import user_model


class AuthMiddleWare:
    """Middleware for authenticating a request before passing it on
    to the mounted django application.
    """

    def __init__(self, app: ASGIApp):
        self.app = app
        self.db_session = SessionLocal()

    def authenticate_request(self, request: Request):
        authorization_header = request.headers.get("authorization")
        if authorization_header is None:
            raise HTTPException(401, "Unauthorized request")
        scheme, token = get_authorization_scheme_param(authorization_header)
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Invalid authorization header scheme")
        try:
            claims = jwt.decode(token, app_config.APP_SECRET)
        except JWTError:
            raise HTTPException(401, "Unauthorized request")
        username = claims["sub"]
        user = user_service.get(self.db_session, username)
        if user is None:
            raise HTTPException(401, "Unauthorized request")
        request.state.user = user

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope, receive, send)
        self.authenticate_request(request)
        await self.app(scope, receive, send)


class WSGIAuthMiddleWare:
    """Middleware for authenticating a request before passing it on
    to the mounted django application.
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    def get_user(self, username: str) -> Optional[user_model.AuthUser]:
        with SessionLocal() as session:
            user: user_model.AuthUser = (
                session.query(user_model.AuthUser)
                .filter(user_model.AuthUser.username == username)
                .one_or_none()
            )
            return user

    def authenticate_request(self, request: Request):
        authorization_header = request.headers.get("authorization")
        if authorization_header is None:
            raise HTTPException(401, "Unauthorized request")
        scheme, token = get_authorization_scheme_param(authorization_header)
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Invalid authorization header scheme")
        try:
            claims = jwt.decode(token, app_config.APP_SECRET)
        except JWTError:
            raise HTTPException(401, "Unauthorized request")
        username = claims["sub"]
        user = self.get_user(username)
        if user is None:
            raise HTTPException(401, "Unauthorized request")
        request.state.user = user

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope, receive, send)
        self.authenticate_request(request)
        await self.app(scope, receive, send)

from typing import Optional
from fastapi.exceptions import HTTPException

from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from jose.exceptions import JWTError
from starlette.types import Scope, Receive, Send, ASGIApp
from jose import jwt
from opencdms_api import models
from opencdms_api.config import settings
from opencdms_api.db import db_session_scope


class AuthMiddleWare:
    """Middleware for authenticating a request before passing it on
    to the mounted django application.
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    def get_user(self, username: str) -> Optional[models.AuthUser]:
        with db_session_scope() as session:
            user: models.AuthUser = (
                session.query(models.AuthUser)
                .filter(models.AuthUser.username == username)
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
            claims = jwt.decode(token, settings.SURFACE_SECRET_KEY)
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

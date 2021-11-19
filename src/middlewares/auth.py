from typing import Optional
from fastapi.exceptions import HTTPException

from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from jose.exceptions import JWTError
from starlette.types import Scope, Receive, Send, ASGIApp
from jose import jwt
from src.apps.auth.services import user_service
from src.config import app_config
from src.apps.auth.db.engine import SessionLocal


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
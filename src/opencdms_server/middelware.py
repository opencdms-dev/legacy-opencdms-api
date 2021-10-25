from fastapi.exceptions import HTTPException

# from passlib.hash import django_pbkdf2_sha256 as handler
# from typing import List, Optional
from fastapi import Request

# from pydantic import BaseModel
# from sqlalchemy.orm.session import Session
# from test_fastapi.db import SessionLocal
# from test_fastapi.models import User
# from test_django.wsgi import application as django_application
from fastapi.security.utils import get_authorization_scheme_param
from starlette.types import Scope, Receive, Send, ASGIApp


class WSGIAuthMiddleWare:
    """Middleware for authenticating a request before passing it on
    to the mounted django application.
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope, receive, send)
        authorization_header = request.headers.get("Authorization")
        if authorization_header is None:
            raise HTTPException(401, "Unauthorized request")
        scheme, token = get_authorization_scheme_param(authorization_header)
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Invalid authorization header scheme")
        # Token Validation code goes here
        if token != "auth_token":
            raise HTTPException(401, "Unauthorized request")
        await self.app(scope, receive, send)

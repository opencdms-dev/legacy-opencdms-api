from typing import Optional
from fastapi.exceptions import HTTPException
import os
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from jose.exceptions import JWTError
from starlette.types import Scope, Receive, Send, ASGIApp
from jose import jwt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.opencdms_api import models
from src.opencdms_api.config import settings
from src.opencdms_api.db import db_session_scope
from src.opencdms_api import climsoft_rbac_config
from src.opencdms_api.schema import CurrentUserSchema
from opencdms.models.climsoft import v4_1_1_core as climsoft_models


class AuthMiddleWare:
    """Middleware for authenticating a request before passing it on
    to the mounted application.
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    def get_user(self, username: str) -> Optional[CurrentUserSchema]:
        with db_session_scope() as session:
            user: models.AuthUser = (
                session.query(models.AuthUser)
                .filter(models.AuthUser.username == username)
                .one_or_none()
            )
            return CurrentUserSchema.from_orm(user) if user is not None else None

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
        return user

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope, receive, send)
        self.authenticate_request(request)
        await self.app(scope, receive, send)


class ClimsoftRBACMiddleware(AuthMiddleWare):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    def get_climsoft_role_for_username(self, username: str):
        climsoft_engine = create_engine(os.getenv("CLIMSOFT_DATABASE_URI"))
        ClimsoftSessionLocal = sessionmaker(climsoft_engine)
        session = ClimsoftSessionLocal()

        role = None

        try:
            user_role = session.query(climsoft_models.ClimsoftUser).filter_by(userName=username).one_or_none()
            role = user_role.userRole
        except Exception as e:
            pass

        session.close()

        return role

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        def extract_resource_from_path(string, sep, start, end):
            string = string.split(sep)
            return sep.join(string[start:end])

        request = Request(scope, receive, send)
        user = None
        if request.url.path not in {
            "/climsoft",
            "/climsoft/openapi.json",
            "/climsoft/"
        }:
            user = self.authenticate_request(request)

        resource_url = extract_resource_from_path(request.url.path, "/", 3, 4)
        required_role = climsoft_rbac_config.required_role_lookup.get(
            resource_url, {}
        ).get(
            request.method.lower()
        )

        if (not required_role) or (self.get_climsoft_role_for_username(user.username) in required_role):
            await self.app(scope, receive, send)
        else:
            raise HTTPException(status_code=403)





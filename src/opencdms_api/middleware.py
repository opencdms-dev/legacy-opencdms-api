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
from src.opencdms_api.schema import CurrentUserSchema, CurrentClimsoftUserSchema
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from fastapi import Header, Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")
climsoft_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/climsoft-auth")


def get_user(username: str) -> Optional[CurrentUserSchema]:
    with db_session_scope() as session:
        user: models.AuthUser = (
            session.query(models.AuthUser)
            .filter(models.AuthUser.username == username)
            .one_or_none()
        )
        return CurrentUserSchema.from_orm(user) \
            if user is not None else None


def get_climsoft_role_for_username(username: str):
    climsoft_engine = create_engine(os.getenv("CLIMSOFT_DATABASE_URI"))
    ClimsoftSessionLocal = sessionmaker(climsoft_engine)
    session = ClimsoftSessionLocal()

    role = None

    try:
        user_role = session.query(climsoft_models.ClimsoftUser).filter_by(
            userName=username
        ).one_or_none()
        role = user_role.userRole
    except Exception as e:
        pass

    session.close()

    return role


def has_required_climsoft_role(username, required_role):
    return get_climsoft_role_for_username(
        username
    ) in required_role


def extract_resource_from_path(string, sep, start, end):
    string = string.split(sep)
    return sep.join(string[start:end])


class AuthMiddleWare:
    """Middleware for authenticating a request before passing it on
    to the mounted application.
    """

    def __init__(self, app: ASGIApp):
        self.app = app

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
        user = CurrentClimsoftUserSchema(username=username)
        if user is None:
            raise HTTPException(401, "Unauthorized request")
        return user

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
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

        if (not required_role) or has_required_climsoft_role(
            user.username, required_role
        ):
            await self.app(scope, receive, send)
        else:
            raise HTTPException(status_code=403)


def get_authorized_climsoft_user(
    request: Request,
    token: str = Depends(climsoft_oauth2_scheme)
):
    try:
        claims = jwt.decode(token, settings.SURFACE_SECRET_KEY)
    except JWTError:
        raise HTTPException(401, "Unauthorized request")

    username = claims["sub"]

    user = CurrentClimsoftUserSchema(username=username)

    if user is None:
        raise HTTPException(401, "Unauthorized request")

    resource_url = extract_resource_from_path(request.url.path, "/", 3, 4)
    required_role = climsoft_rbac_config.required_role_lookup.get(
        resource_url, {}
    ).get(
        request.method.lower()
    )

    if required_role and not has_required_climsoft_role(
        user.username, required_role
    ):
        raise HTTPException(status_code=403)

    return user

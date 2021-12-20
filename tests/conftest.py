from fastapi.applications import FastAPI
import pytest
from datetime import datetime, timedelta
from jose import jwt
from typing import Dict, Generator

from sqlalchemy.orm.session import Session
from opencdms_api.db import SessionLocal
from opencdms_api.models import AuthUser
from passlib.hash import django_pbkdf2_sha256 as handler
from opencdms_api.config import settings
from opencdms_api.main import get_app
from fastapi.testclient import TestClient
from main import app as oapp

@pytest.fixture
def app() -> FastAPI:
    return get_app()

@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def session() -> Session:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def user(session: Session) -> Generator[AuthUser, None, None]:
    user = AuthUser(
        password=handler.hash("password"),
        is_superuser=False,
        username="john_doe",
        first_name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
    )
    session.add(user)
    session.commit()
    yield user
    session.delete(user)
    session.commit()


@pytest.fixture
def user_access_token(user: AuthUser) -> str:
    access_token = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=24)},
        key=settings.SURFACE_SECRET_KEY,
    )
    return access_token

@pytest.fixture
def user_auth_header(user_access_token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {user_access_token}"}

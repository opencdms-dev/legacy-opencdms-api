from fastapi.applications import FastAPI
import pytest
from datetime import datetime, timedelta
from jose import jwt
from typing import Dict, Generator

from sqlalchemy.orm.session import Session
from opencdms_server.db import SessionLocal
from opencdms_server.models import AuthUser
from passlib.hash import django_pbkdf2_sha256 as handler
from opencdms_server.config import settings
from opencdms_server.main import get_app
from fastapi.testclient import TestClient


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
def user_auth_header(user: AuthUser) -> Dict[str, str]:
    access_token = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=24)},
        key=settings.SECRET_KEY,
    )
    return {"Authorization": f"Bearer {access_token}"}

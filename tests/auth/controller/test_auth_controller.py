import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from src.apps.auth.db.models import user_model
from src.apps.auth.db.engine import db_engine
from passlib.hash import django_pbkdf2_sha256 as handler
from src.apps.auth.schemas import auth_schema
from tests.datagen.auth import user as auth_user
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f'''
                TRUNCATE TABLE {user_model.AuthUser.__tablename__} RESTART IDENTITY CASCADE
            ''').execution_options(autocommit=True))


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f'''
                TRUNCATE TABLE {user_model.AuthUser.__tablename__} RESTART IDENTITY CASCADE
            ''').execution_options(autocommit=True))


@pytest.fixture
def get_user():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    user = user_model.AuthUser(
        username=fake.user_name(),
        password=handler.hash("password"),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email()
    )
    session.add(user)
    session.commit()
    yield user
    session.close()


def test_should_signup_successfully(test_app: TestClient):
    response = test_app.post("/api/auth/v1/sign-up", json=auth_user.get_valid_signup_input().dict())
    print(response.json())
    assert response.status_code == 200


def test_should_signin_successfully(test_app: TestClient, get_user: user_model.AuthUser):
    response = test_app.post(f"/api/auth/v1/sign-in", json=auth_user.get_valid_signin_input(username=get_user.username).dict())
    response_data = response.json()
    assert response.status_code == 200
    assert 'access_token' in response_data and response_data['access_token'] != ''


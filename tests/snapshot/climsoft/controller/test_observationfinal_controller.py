import pytest
from faker import Faker
from fastapi.testclient import TestClient
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from passlib.hash import django_pbkdf2_sha256 as handler
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import text as sa_text

from apps.auth.db.engine import db_engine as auth_db_engine
from apps.auth.db.models import user_model
from apps.climsoft.schemas import observationfinal_schema

fake = Faker()


def setup_module(module):
    with auth_db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            auth_db_engine.execute(sa_text(f'''
                TRUNCATE TABLE {user_model.AuthUser.__tablename__} RESTART IDENTITY CASCADE
            ''').execution_options(autocommit=True))

    AuthSession = sessionmaker(bind=auth_db_engine)
    auth_session = AuthSession()
    user = user_model.AuthUser(
        username="testuser",
        password=handler.hash("password"),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email()
    )
    auth_session.add(user)
    auth_session.commit()
    auth_session.close()


def teardown_module(module):
    with auth_db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            auth_db_engine.execute(sa_text(f'''
                TRUNCATE TABLE {user_model.AuthUser.__tablename__} RESTART IDENTITY CASCADE
            ''').execution_options(autocommit=True))


@pytest.fixture
def get_access_token(user_access_token: str) -> str:
    return user_access_token


def test_should_return_first_five_observation_finals(client: TestClient, get_access_token: str):
    response = client.get("/climsoft/v1/observation-finals", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5


def test_should_return_single_observation_final(client: TestClient,
                                                get_access_token: str):
    response = client.get(
        f"/climsoft/v1/observation-finals/67774010/4/2000-01-19 06:00:00",
        headers={
            "Authorization": f"Bearer {get_access_token}"
        })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, observationfinal_schema.ObservationFinal)

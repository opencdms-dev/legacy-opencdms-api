import pytest
from faker import Faker
from fastapi.testclient import TestClient
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from passlib.hash import django_pbkdf2_sha256 as handler
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql import text as sa_text

from apps.auth.db.engine import db_engine as auth_db_engine
from apps.auth.db.models import user_model
from apps.climsoft.schemas import stationelement_schema

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


#
#
# def test_should_return_first_five_station_elements(client: TestClient, get_access_token: str):
#     response = client.get("/climsoft/v1/station-elements", params={"limit": 5}, headers={
#         "Authorization": f"Bearer {get_access_token}"
#     })
#     assert response.status_code == 200
#     response_data = response.json()
#     assert len(response_data["result"]) == 5
#     for s in response_data["result"]:
#         isinstance(s, stationelement_schema.StationElement)
#
#
# def test_should_return_single_station_element(client: TestClient, get_access_token: str):
#     response = client.get(f"/climsoft/v1/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}", headers={
#         "Authorization": f"Bearer {get_access_token}"
#     })
#     assert response.status_code == 200
#     response_data = response.json()
#     assert len(response_data["result"]) == 1
#     for s in response_data["result"]:
#         isinstance(s, stationelement_schema.StationElement)
#
#

import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from apps.climsoft.db.engine import db_engine
from apps.climsoft.schemas import obselement_schema
from datagen.climsoft import obselement as climsoft_obselement
from faker import Faker
from fastapi.testclient import TestClient
from apps.auth.db.engine import db_engine as auth_db_engine
from apps.auth.db.models import user_model
from passlib.hash import django_pbkdf2_sha256 as handler

fake = Faker()


def setup_module(module):
    with auth_db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            auth_db_engine.execute(sa_text(f'''
                TRUNCATE TABLE {user_model.AuthUser.__tablename__} RESTART IDENTITY CASCADE
            ''').execution_options(autocommit=True))
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))

    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    for i in range(1, 11):
        db_session.add(climsoft_models.Obselement(
            **climsoft_obselement.get_valid_obselement_input().dict()
        ))
    db_session.commit()
    db_session.close()

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
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))


@pytest.fixture
def get_access_token(user_access_token: str) -> str:
    return user_access_token


@pytest.fixture
def get_obselement():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    obselement = climsoft_models.Obselement(**climsoft_obselement.get_valid_obselement_input().dict())
    session.add(obselement)
    session.commit()
    yield obselement
    session.close()


def test_should_return_first_five_obselements(client: TestClient, get_access_token: str):
    response = client.get("/climsoft/v1/obselements", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, obselement_schema.ObsElement)


def test_should_return_single_station(client: TestClient, get_obselement: climsoft_models.Obselement, get_access_token: str):
    response = client.get(f"/climsoft/v1/obselements/{get_obselement.elementId}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, obselement_schema.ObsElement)


def test_should_create_a_station(client: TestClient, get_access_token: str):
    obselement_data = climsoft_obselement.get_valid_obselement_input().dict(by_alias=True)
    response = client.post("/climsoft/v1/obselements", data=json.dumps(obselement_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, obselement_schema.ObsElement)


def test_should_raise_validation_error(client: TestClient, get_access_token: str):
    obselement_data = climsoft_obselement.get_valid_obselement_input().dict()
    response = client.post("/climsoft/v1/obselements", data=json.dumps(obselement_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_station(client: TestClient, get_obselement, get_access_token: str):
    obselement_data = obselement_schema.ObsElement.from_orm(get_obselement).dict(by_alias=True)
    element_id = obselement_data.pop("element_id")
    updates = {**obselement_data, "element_name": "updated name"}
    response = client.put(f"/climsoft/v1/obselements/{element_id}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["element_name"] == updates["element_name"]


def test_should_delete_station(client: TestClient, get_obselement, get_access_token: str):
    obselement_data = obselement_schema.ObsElement.from_orm(get_obselement).dict(by_alias=True)
    element_id = obselement_data.pop("element_id")

    response = client.delete(f"/climsoft/v1/obselements/{element_id}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200

    response = client.get(f"/climsoft/v1/obselements/{element_id}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })

    assert response.status_code == 404

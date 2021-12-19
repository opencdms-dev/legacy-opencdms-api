import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from apps.climsoft.db.engine import db_engine
from apps.climsoft.schemas import acquisitiontype_schema
from datagen.climsoft import acquisitiontype as climsoft_acquisition_type
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
                TRUNCATE TABLE {climsoft_models.Acquisitiontype.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))

    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    for i in range(1, 11):
        db_session.add(climsoft_models.Acquisitiontype(
            **climsoft_acquisition_type.get_valid_acquisition_type_input().dict()
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
                TRUNCATE TABLE {climsoft_models.Acquisitiontype.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))


@pytest.fixture
def get_access_token(user_access_token: str) -> str:
    return user_access_token


@pytest.fixture
def get_acquisition_type():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    acquisition_type = climsoft_models.Acquisitiontype(**climsoft_acquisition_type.get_valid_acquisition_type_input().dict())
    session.add(acquisition_type)
    session.commit()
    yield acquisition_type
    session.close()


def test_should_return_first_five_acquisition_types(client: TestClient, get_access_token: str):
    response = client.get("/climsoft/v1/acquisition-types", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, acquisitiontype_schema.AcquisitionType)


def test_should_return_single_acquisition_type(client: TestClient, get_acquisition_type: climsoft_models.Acquisitiontype, get_access_token: str):
    response = client.get(f"/climsoft/v1/acquisition-types/{get_acquisition_type.code}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, acquisitiontype_schema.AcquisitionType)


def test_should_create_a_acquisition_type(client: TestClient, get_access_token: str):
    acquisition_type_data = climsoft_acquisition_type.get_valid_acquisition_type_input().dict(by_alias=True)
    response = client.post("/climsoft/v1/acquisition-types", data=json.dumps(acquisition_type_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, acquisitiontype_schema.AcquisitionType)


def test_should_raise_validation_error(client: TestClient, get_access_token: str):
    acquisition_type_data = {"code": "asd", "description": "aa aa a"}
    response = client.post("/climsoft/v1/acquisition-types", data=json.dumps(acquisition_type_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_acquisition_type(client: TestClient, get_acquisition_type, get_access_token: str):
    acquisition_type_data = acquisitiontype_schema.AcquisitionType.from_orm(get_acquisition_type).dict(by_alias=True)
    code = acquisition_type_data.pop("code")
    updates = {**acquisition_type_data, "description": "updated description"}

    response = client.put(f"/climsoft/v1/acquisition-types/{code}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["description"] == updates["description"]


def test_should_delete_acquisition_type(client: TestClient, get_acquisition_type, get_access_token: str):
    acquisition_type_data = acquisitiontype_schema.AcquisitionType.from_orm(get_acquisition_type).dict(by_alias=True)
    code = acquisition_type_data.pop("code")

    response = client.delete(f"/climsoft/v1/acquisition-types/{code}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200

    response = client.get(f"/climsoft/v1/acquisition-types/{code}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 404

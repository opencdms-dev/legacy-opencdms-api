import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.apps.climsoft.db.engine import db_engine
from src.apps.climsoft.schemas import qcstatusdefinition_schema
from tests.datagen.climsoft import qcstatusdefinition as climsoft_qcstatusdefinition
from faker import Faker
from fastapi.testclient import TestClient
from src.apps.auth.db.engine import db_engine as auth_db_engine
from src.apps.auth.db.models import user_model
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
                TRUNCATE TABLE {climsoft_models.Qcstatusdefinition.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))

    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    for i in range(1, 11):
        db_session.add(climsoft_models.Qcstatusdefinition(
            **climsoft_qcstatusdefinition.get_valid_qc_status_definition_input().dict()
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
                TRUNCATE TABLE {climsoft_models.Qcstatusdefinition.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))


@pytest.fixture
def get_access_token(test_app: TestClient):
    sign_in_data = {"username": "testuser", "password": "password", "scope": ""}
    response = test_app.post("/api/auth/v1/sign-in", data=sign_in_data)
    response_data = response.json()
    return response_data['access_token']


@pytest.fixture
def get_qc_status_definition():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    qc_status_definition = climsoft_models.Qcstatusdefinition(**climsoft_qcstatusdefinition.get_valid_qc_status_definition_input().dict())
    session.add(qc_status_definition)
    session.commit()
    yield qc_status_definition
    session.close()


def test_should_return_first_five_qc_status_definitions(test_app: TestClient, get_access_token: str):
    response = test_app.get("/api/climsoft/v1/qc-status-definitions", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5


def test_should_return_single_qc_status_definition(test_app: TestClient, get_qc_status_definition: climsoft_models.Qcstatusdefinition, get_access_token: str):
    response = test_app.get(f"/api/climsoft/v1/qc-status-definitions/{get_qc_status_definition.code}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1


def test_should_create_a_qc_status_definition(test_app: TestClient, get_access_token: str):
    qc_status_definition_data = climsoft_qcstatusdefinition.get_valid_qc_status_definition_input().dict(by_alias=True)
    response = test_app.post("/api/climsoft/v1/qc-status-definitions", data=json.dumps(qc_status_definition_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1


def test_should_raise_validation_error(test_app: TestClient, get_access_token: str):
    qc_status_definition_data = {"aaa": "bbbbbbb"}
    response = test_app.post("/api/climsoft/v1/qc-status-definitions", data=json.dumps(qc_status_definition_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_qc_status_definition(test_app: TestClient, get_qc_status_definition, get_access_token: str):
    qc_status_definition_data = qcstatusdefinition_schema.QCStatusDefinition.from_orm(get_qc_status_definition).dict(by_alias=True)
    code = qc_status_definition_data.pop("code")
    updates = {**qc_status_definition_data, "description": "updated name"}

    response = test_app.put(f"/api/climsoft/v1/qc-status-definitions/{code}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["description"] == updates["description"]


def test_should_delete_qc_status_definition(test_app: TestClient, get_qc_status_definition, get_access_token: str):
    qc_status_definition_data = qcstatusdefinition_schema.QCStatusDefinition.from_orm(get_qc_status_definition).dict(by_alias=True)
    code = qc_status_definition_data.pop("code")

    response = test_app.delete(f"/api/climsoft/v1/qc-status-definitions/{code}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200

    response = test_app.get(f"/api/climsoft/v1/qc-status-definitions/{code}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 404

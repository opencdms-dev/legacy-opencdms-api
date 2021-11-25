import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.apps.climsoft.db.engine import db_engine
from src.apps.climsoft.schemas import data_form_schema
from tests.datagen.climsoft import data_form as climsoft_data_form
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
                TRUNCATE TABLE {climsoft_models.DataForm.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))

    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    for i in range(1, 11):
        db_session.add(climsoft_models.DataForm(
            **climsoft_data_form.get_valid_data_form_input().dict()
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
                TRUNCATE TABLE {climsoft_models.DataForm.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))


@pytest.fixture
def get_access_token(test_app: TestClient):
    sign_in_data = {"username": "testuser", "password": "password", "scope": ""}
    response = test_app.post("/api/auth/v1/sign-in", data=sign_in_data)
    response_data = response.json()
    return response_data['access_token']


@pytest.fixture
def get_data_form():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    data_form = climsoft_models.DataForm(**climsoft_data_form.get_valid_data_form_input().dict())
    session.add(data_form)
    session.commit()
    yield data_form
    session.close()


def test_should_return_first_five_data_forms(test_app: TestClient, get_access_token: str):
    response = test_app.get("/api/climsoft/v1/data-forms", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, data_form_schema.DataForm)


def test_should_return_single_data_form(test_app: TestClient, get_data_form: climsoft_models.DataForm, get_access_token: str):
    response = test_app.get(f"/api/climsoft/v1/data-forms/{get_data_form.form_name}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, data_form_schema.DataForm)


def test_should_create_a_data_form(test_app: TestClient, get_access_token: str):
    data_form_data = climsoft_data_form.get_valid_data_form_input().dict(by_alias=True)
    response = test_app.post("/api/climsoft/v1/data-forms", data=json.dumps(data_form_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, data_form_schema.DataForm)


def test_should_raise_validation_error(test_app: TestClient, get_access_token: str):
    data_form_data = climsoft_data_form.get_valid_data_form_input().dict().pop("form_name")
    response = test_app.post("/api/climsoft/v1/data-forms", data=json.dumps(data_form_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_data_form(test_app: TestClient, get_data_form, get_access_token: str):
    data_form_data = data_form_schema.DataForm.from_orm(get_data_form).dict(by_alias=True)
    form_name = data_form_data.pop("form_name")
    updates = {**data_form_data, "table_name": "updated name"}

    response = test_app.put(f"/api/climsoft/v1/data-forms/{form_name}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["table_name"] == updates["table_name"]


def test_should_delete_data_form(test_app: TestClient, get_data_form, get_access_token: str):
    data_form_data = data_form_schema.DataForm.from_orm(get_data_form).dict(by_alias=True)
    form_name = data_form_data.pop("form_name")

    response = test_app.delete(f"/api/climsoft/v1/data-forms/{form_name}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200

    response = test_app.get(f"/api/climsoft/v1/data-forms/{form_name}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 404
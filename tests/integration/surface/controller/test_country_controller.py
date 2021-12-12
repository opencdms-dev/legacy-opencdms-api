import json
import os
import django
import pytest
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connection
from sqlalchemy.orm.session import sessionmaker
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import text as sa_text
from config import app_config
from datagen.surface import country
from apps.auth.db.engine import db_engine as auth_db_engine
from apps.auth.db.models import user_model
from passlib.hash import django_pbkdf2_sha256 as handler

fake = Faker()


def setup_module(module):
    with auth_db_engine.connect().execution_options(autocommit=True) as _connection:
        with _connection.begin():
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

    try:
        settings.configure(
            DATABASES={
                "default": {
                    "ENGINE": "django.contrib.gis.db.backends.postgis",
                    "NAME": app_config.SURFACE_DB_NAME,
                    "USER": app_config.SURFACE_DB_USER,
                    "PASSWORD": app_config.SURFACE_DB_PASSWORD,
                    "HOST": app_config.SURFACE_DB_HOST,
                    "PORT": app_config.SURFACE_DB_PORT
                }
            },
            DEFAULT_AUTO_FIELD="django.db.models.AutoField",
            BASE_DIR=app_config.BASE_DIR,
            INSTALLED_APPS=(
                "apps.surface",
                "django.contrib.auth",
                "django.contrib.gis",
                "django.contrib.contenttypes"
            )
        )
    except RuntimeError:
        pass

    django.setup()

    execute_from_command_line([
        os.path.abspath(__file__),
        "makemigrations",
        "surface"
    ])
    execute_from_command_line([
        os.path.abspath(__file__),
        "migrate"
    ])

    from apps.surface import models

    with connection.cursor() as cursor:
        cursor.execute(f'''
            TRUNCATE TABLE {models.Country._meta.db_table} RESTART IDENTITY CASCADE
        ''')


def teardown_module(module):
    from apps.surface import models
    with auth_db_engine.connect().execution_options(autocommit=True) as _connection:
        with _connection.begin():
            auth_db_engine.execute(sa_text(f'''
                TRUNCATE TABLE {user_model.AuthUser.__tablename__} RESTART IDENTITY CASCADE
            ''').execution_options(autocommit=True))
    with connection.cursor() as cursor:
        cursor.execute(f'''
            TRUNCATE TABLE {models.Country._meta.db_table} RESTART IDENTITY CASCADE
        ''')


@pytest.fixture
def get_access_token(test_app: TestClient):
    sign_in_data = {"username": "testuser", "password": "password", "scope": ""}
    response = test_app.post("/api/auth/v1/sign-in", data=sign_in_data)
    response_data = response.json()
    return response_data['access_token']


@pytest.fixture
def get_country():
    from apps.surface import models
    _country = models.Country(**country.get_valid_country_input().dict())
    _country.save()
    yield _country


def test_should_return_single_country(test_app: TestClient, get_country, get_access_token: str):
    from apps.surface.schemas import country_schema
    response = test_app.get(f"/api/surface/v1/countries/{get_country.name}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, country_schema.Country)


def test_should_create_a_country(test_app: TestClient, get_access_token: str):
    from apps.surface.schemas import country_schema
    country_data = country.get_valid_country_input().dict()
    response = test_app.post("/api/surface/v1/countries", data=json.dumps(country_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, country_schema.Country)


def test_should_raise_validation_error(test_app: TestClient, get_access_token: str):
    country_data = {"code": "aaaaaaa", "name": "bbbbbbbbb"}
    response = test_app.post("/api/surface/v1/countries", data=json.dumps(country_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_country(test_app: TestClient, get_country, get_access_token: str):
    from apps.surface.schemas import country_schema
    country_data = country_schema.Country.from_django(get_country).dict(by_alias=True)
    name = country_data.pop("name")
    updates = {"code": "ab"}

    response = test_app.put(f"/api/surface/v1/countries/{name}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["code"] == updates["code"]


def test_should_delete_country(test_app: TestClient, get_country, get_access_token: str):
    from apps.surface.schemas import country_schema
    country_data = country_schema.Country.from_django(get_country).dict(by_alias=True)
    name = country_data.pop("name")

    response = test_app.delete(f"/api/surface/v1/countries/{name}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200

    response = test_app.get(f"/api/surface/v1/countries/{name}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 404

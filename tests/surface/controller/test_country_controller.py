import json
import os

import django
import pytest
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connection
from faker import Faker
from fastapi.testclient import TestClient

from src.config import app_config
from tests.datagen.surface import country

fake = Faker()


def setup_module(module):

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
                "src.apps.surface",
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

    from src.apps.surface import models

    with connection.cursor() as cursor:
        cursor.execute(f'''
            TRUNCATE TABLE {models.Country._meta.db_table} RESTART IDENTITY CASCADE
        ''')


def teardown_module(module):
    from src.apps.surface import models
    with connection.cursor() as cursor:
        cursor.execute(f'''
            TRUNCATE TABLE {models.Country._meta.db_table} RESTART IDENTITY CASCADE
        ''')


@pytest.fixture
def get_country():
    from src.apps.surface import models
    models.Country(**country.get_valid_country_input().dict()).save()


def test_should_return_single_country(test_app: TestClient, get_country):
    from src.apps.surface.schemas import country_schema
    response = test_app.get(f"/api/climsoft/v1/countries/{get_country.countryId}")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, country_schema.Country)


def test_should_create_a_country(test_app: TestClient):
    from src.apps.surface.schemas import country_schema
    country_data = country.get_valid_country_input().dict(by_alias=True)
    response = test_app.post("/api/climsoft/v1/countries", data=json.dumps(country_data, default=str))
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, country_schema.Country)


def test_should_raise_validation_error(test_app: TestClient):
    country_data = country.get_valid_country_input().dict()
    response = test_app.post("/api/climsoft/v1/countries", data=json.dumps(country_data, default=str))
    assert response.status_code == 422


def test_should_update_country(test_app: TestClient, get_country):
    from src.apps.surface.schemas import country_schema
    country_data = country_schema.Country.from_django(get_country).dict(by_alias=True)
    name = country_data.pop("name")
    updates = {**country_data, "name": fake.country()}

    response = test_app.put(f"/api/climsoft/v1/countries/{name}", data=json.dumps(updates, default=str))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["name"] == updates["name"]


def test_should_delete_country(test_app: TestClient, get_country):
    from src.apps.surface.schemas import country_schema
    country_data = country_schema.Country.from_django(get_country).dict(by_alias=True)
    name = country_data.pop("name")

    response = test_app.delete(f"/api/climsoft/v1/countries/{name}")
    assert response.status_code == 200

    response = test_app.get(f"/api/climsoft/v1/countries/{name}")
    assert response.status_code == 404

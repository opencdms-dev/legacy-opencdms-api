import datetime
import json
import uuid

import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from apps.climsoft.db.engine import db_engine
from apps.climsoft.schemas import stationqualifier_schema
from datagen.climsoft import stationqualifier as climsoft_station_qualifier, station as climsoft_station
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
                TRUNCATE TABLE {climsoft_models.Stationqualifier.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))

    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    for i in range(1, 11):
        station = climsoft_models.Station(
            **climsoft_station.get_valid_station_input().dict()
        )
        db_session.add(station)
        db_session.commit()

        db_session.add(climsoft_models.Stationqualifier(
            **climsoft_station_qualifier.get_valid_station_qualifier_input(station_id=station.stationId).dict()
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
                TRUNCATE TABLE {climsoft_models.Stationqualifier.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))


@pytest.fixture
def get_access_token(user_access_token: str) -> str:
    return user_access_token


@pytest.fixture
def get_station():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    station = climsoft_models.Station(**climsoft_station.get_valid_station_input().dict())
    session.add(station)
    session.commit()
    yield station
    session.close()


@pytest.fixture
def get_station_qualifier(get_station: climsoft_models.Station):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    station_qualifier = climsoft_models.Stationqualifier(**climsoft_station_qualifier.get_valid_station_qualifier_input(station_id=get_station.stationId).dict())
    session.add(station_qualifier)
    session.commit()
    yield station_qualifier
    session.close()


def test_should_return_first_five_station_qualifiers(client: TestClient, get_access_token: str):
    response = client.get("/climsoft/v1/station-qualifiers", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5


def test_should_return_single_station_qualifier(client: TestClient, get_station_qualifier: climsoft_models.Stationqualifier, get_access_token: str):
    response = client.get(f"/climsoft/v1/station-qualifiers/{get_station_qualifier.qualifier}/{get_station_qualifier.qualifierBeginDate}/{get_station_qualifier.qualifierEndDate}/{get_station_qualifier.belongsTo}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1


def test_should_create_a_station_qualifier(client: TestClient, get_station: climsoft_models.Station, get_access_token: str):
    station_qualifier_data = climsoft_station_qualifier.get_valid_station_qualifier_input(station_id=get_station.stationId).dict(by_alias=True)
    response = client.post("/climsoft/v1/station-qualifiers", data=json.dumps(station_qualifier_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1


def test_should_raise_validation_error(client: TestClient, get_station: climsoft_models.Station, get_access_token: str):
    station_qualifier_data = climsoft_station_qualifier.get_valid_station_qualifier_input(station_id=get_station.stationId).dict()
    response = client.post("/climsoft/v1/station-qualifiers", data=json.dumps(station_qualifier_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_station_qualifier(client: TestClient, get_station_qualifier: climsoft_models.Stationqualifier, get_access_token: str):
    station_qualifier_data = stationqualifier_schema.StationQualifier.from_orm(get_station_qualifier).dict(by_alias=True)
    belongs_to = station_qualifier_data.pop("belongs_to")
    qualifier_begin_date = station_qualifier_data.pop("qualifier_begin_date")
    qualifier_end_date = station_qualifier_data.pop("qualifier_end_date")
    qualifier = station_qualifier_data.pop("qualifier")
    updates = {**station_qualifier_data, "station_timezone": 1}

    response = client.put(f"/climsoft/v1/station-qualifiers/{qualifier}/{qualifier_begin_date}/{qualifier_end_date}/{belongs_to}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["station_timezone"] == updates["station_timezone"]


def test_should_delete_station_qualifier(client: TestClient, get_station_qualifier: stationqualifier_schema.StationQualifier, get_access_token: str):
    station_qualifier_data = stationqualifier_schema.StationQualifier.from_orm(get_station_qualifier).dict(by_alias=True)
    belongs_to = station_qualifier_data.pop("belongs_to")
    qualifier_begin_date = station_qualifier_data.pop("qualifier_begin_date")
    qualifier_end_date = station_qualifier_data.pop("qualifier_end_date")
    qualifier = station_qualifier_data.pop("qualifier")
    response = client.delete(f"/climsoft/v1/station-qualifiers/{qualifier}/{qualifier_begin_date}/{qualifier_end_date}/{belongs_to}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200

    response = client.get(f"/climsoft/v1/station-qualifiers/{qualifier}/{qualifier_begin_date}/{qualifier_end_date}/{belongs_to}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })

    assert response.status_code == 404

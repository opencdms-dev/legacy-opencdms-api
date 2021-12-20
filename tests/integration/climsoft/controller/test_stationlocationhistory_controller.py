import datetime
import json
import uuid

import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from apps.climsoft.db.engine import db_engine
from apps.climsoft.schemas import stationlocationhistory_schema
from datagen.climsoft import stationlocationhistory as climsoft_station_location_history, station as climsoft_station
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
                TRUNCATE TABLE {climsoft_models.Stationlocationhistory.__tablename__};
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

        db_session.add(climsoft_models.Stationlocationhistory(
            **climsoft_station_location_history.get_valid_station_location_history_input(station_id=station.stationId).dict()
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
                TRUNCATE TABLE {climsoft_models.Stationlocationhistory.__tablename__};
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
def get_station_location_history(get_station: climsoft_models.Station):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    station_location_history = climsoft_models.Stationlocationhistory(**climsoft_station_location_history.get_valid_station_location_history_input(station_id=get_station.stationId).dict())
    session.add(station_location_history)
    session.commit()
    yield station_location_history
    session.close()


def test_should_return_first_five_station_location_histories(client: TestClient, get_access_token: str):
    response = client.get("/climsoft/v1/station-location-histories", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5


def test_should_return_single_station_location_history(client: TestClient, get_station_location_history: climsoft_models.Stationlocationhistory, get_access_token: str):
    response = client.get(f"/climsoft/v1/station-location-histories/{get_station_location_history.belongsTo}/{get_station_location_history.openingDatetime}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1


def test_should_create_a_station_location_history(client: TestClient, get_station: climsoft_models.Station, get_access_token: str):
    station_location_history_data = climsoft_station_location_history.get_valid_station_location_history_input(station_id=get_station.stationId).dict(by_alias=True)
    response = client.post("/climsoft/v1/station-location-histories", data=json.dumps(station_location_history_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1


def test_should_raise_validation_error(client: TestClient, get_station: climsoft_models.Station, get_access_token: str):
    station_location_history_data = climsoft_station_location_history.get_valid_station_location_history_input(station_id=get_station.stationId).dict()
    response = client.post("/climsoft/v1/station-location-histories", data=json.dumps(station_location_history_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_station_location_history(client: TestClient, get_station_location_history: climsoft_models.Stationlocationhistory, get_access_token: str):
    station_location_history_data = stationlocationhistory_schema.StationLocationHistory.from_orm(get_station_location_history).dict(by_alias=True)
    belongs_to = station_location_history_data.pop("belongs_to")
    opening_datetime = station_location_history_data.pop("opening_datetime")
    updates = {**station_location_history_data, "authority": uuid.uuid4().hex}

    response = client.put(f"/climsoft/v1/station-location-histories/{belongs_to}/{opening_datetime}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["authority"] == updates["authority"]


def test_should_delete_station_location_history(client: TestClient, get_station_location_history, get_access_token: str):
    station_location_history_data = stationlocationhistory_schema.StationLocationHistory.from_orm(get_station_location_history).dict(by_alias=True)
    belongs_to = station_location_history_data.pop("belongs_to")
    opening_datetime = station_location_history_data.pop("opening_datetime")

    response = client.delete(f"/climsoft/v1/station-location-histories/{belongs_to}/{opening_datetime}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200

    response = client.get(f"/climsoft/v1/station-location-histories/{belongs_to}/{opening_datetime}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })

    assert response.status_code == 404

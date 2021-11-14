import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.db.engine import db_engine
from src.apps.climsoft.schemas import station_schema
from tests.datagen.climsoft import station as climsoft_station
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))

    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    for i in range(1, 11):
        db_session.add(climsoft_models.Station(
            **climsoft_station.get_valid_station_input().dict()
        ))
    db_session.commit()
    db_session.close()


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))


@pytest.fixture
def get_station():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    station = climsoft_models.Station(**climsoft_station.get_valid_station_input().dict())
    session.add(station)
    session.commit()
    yield station
    session.close()


def test_should_return_first_five_stations(test_app: TestClient):
    response = test_app.get("/api/v1/climsoft/stations", params={"limit": 5})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, station_schema.Station)


def test_should_return_single_station(test_app: TestClient, get_station: climsoft_models.Station):
    response = test_app.get(f"/api/v1/climsoft/stations/{get_station.stationId}")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, station_schema.Station)


def test_should_create_a_station(test_app: TestClient):
    station_data = climsoft_station.get_valid_station_input().dict(by_alias=True)
    response = test_app.post("/api/v1/climsoft/stations", data=json.dumps(station_data, default=str))
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, station_schema.Station)


def test_should_raise_validation_error(test_app: TestClient):
    station_data = climsoft_station.get_valid_station_input().dict()
    response = test_app.post("/api/v1/climsoft/stations", data=json.dumps(station_data, default=str))
    assert response.status_code == 422


def test_should_update_station(test_app: TestClient, get_station):
    station_data = station_schema.Station.from_orm(get_station).dict(by_alias=True)
    station_id = station_data.pop("station_id")
    updates = {**station_data, "station_name": "updated name"}

    response = test_app.put(f"/api/v1/climsoft/stations/{station_id}", data=json.dumps(updates, default=str))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["station_name"] == updates["station_name"]


def test_should_delete_station(test_app: TestClient, get_station):
    station_data = station_schema.Station.from_orm(get_station).dict(by_alias=True)
    station_id = station_data.pop("station_id")

    response = test_app.delete(f"/api/v1/climsoft/stations/{station_id}")
    assert response.status_code == 200

    response = test_app.get(f"/api/v1/climsoft/stations/{station_id}")
    assert response.status_code == 404

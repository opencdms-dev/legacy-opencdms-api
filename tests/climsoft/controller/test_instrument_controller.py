import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.apps.climsoft.db.engine import db_engine
from src.apps.climsoft.schemas import instrument_schema
from tests.datagen.climsoft import instrument as climsoft_instrument, station as climsoft_station
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Instrument.__tablename__};
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

        db_session.add(climsoft_models.Instrument(
            **climsoft_instrument.get_valid_instrument_input(station_id=station.stationId).dict()
        ))
        db_session.commit()
    db_session.close()


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Instrument.__tablename__};
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


@pytest.fixture
def get_instrument(get_station: climsoft_models.Station):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    instrument = climsoft_models.Instrument(**climsoft_instrument.get_valid_instrument_input(station_id=get_station.stationId).dict())
    session.add(instrument)
    session.commit()
    yield instrument
    session.close()


def test_should_return_first_five_instruments(test_app: TestClient):
    response = test_app.get("/api/climsoft/v1/instruments", params={"limit": 5})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, instrument_schema.Instrument)


def test_should_return_single_instrument(test_app: TestClient, get_instrument: climsoft_models.Instrument):
    response = test_app.get(f"/api/climsoft/v1/instruments/{get_instrument.instrumentId}")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, instrument_schema.Instrument)


def test_should_create_a_instrument(test_app: TestClient, get_station: climsoft_models.Station):
    instrument_data = climsoft_instrument.get_valid_instrument_input(station_id=get_station.stationId).dict(by_alias=True)
    response = test_app.post("/api/climsoft/v1/instruments", data=json.dumps(instrument_data, default=str))
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, instrument_schema.Instrument)


def test_should_raise_validation_error(test_app: TestClient, get_station: climsoft_models.Station):
    instrument_data = climsoft_instrument.get_valid_instrument_input(station_id=get_station.stationId).dict()
    response = test_app.post("/api/climsoft/v1/instruments", data=json.dumps(instrument_data, default=str))
    assert response.status_code == 422


def test_should_update_instrument(test_app: TestClient, get_instrument: climsoft_models.Instrument):
    instrument_data = instrument_schema.Instrument.from_orm(get_instrument).dict(by_alias=True)
    instrument_id = instrument_data.pop("instrument_id")
    updates = {**instrument_data, "instrument_name": "updated name"}

    response = test_app.put(f"/api/climsoft/v1/instruments/{instrument_id}", data=json.dumps(updates, default=str))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["instrument_name"] == updates["instrument_name"]


def test_should_delete_instrument(test_app: TestClient, get_instrument):
    instrument_data = instrument_schema.Instrument.from_orm(get_instrument).dict(by_alias=True)
    instrument_id = instrument_data.pop("instrument_id")

    response = test_app.delete(f"/api/climsoft/v1/instruments/{instrument_id}")
    assert response.status_code == 200

    response = test_app.get(f"/api/climsoft/v1/instruments/{instrument_id}")
    assert response.status_code == 404

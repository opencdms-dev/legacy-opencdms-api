import datetime
import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.db.engine import db_engine
from src.apps.climsoft.schemas import stationelement_schema
from tests.datagen.climsoft import stationelement as climsoft_station_element, obsscheduleclass as climsoft_obsscheduleclass, obselement as climsoft_obselement, station as climsoft_station, instrument as climsoft_instrument
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Stationelement.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                TRUNCATE TABLE {climsoft_models.Obsscheduleclas.__tablename__};
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
                TRUNCATE TABLE {climsoft_models.Stationelement.__tablename__};
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

        obs_element = climsoft_models.Obselement(
            **climsoft_obselement.get_valid_obselement_input().dict()
        )
        db_session.add(obs_element)
        db_session.commit()

        obs_schedule_class = climsoft_models.Obsscheduleclas(
            **climsoft_obsscheduleclass.get_valid_obs_schedule_class_input(station_id=station.stationId).dict()
        )
        db_session.add(obs_schedule_class)
        db_session.commit()

        instrument = climsoft_models.Instrument(
            **climsoft_instrument.get_valid_instrument_input(station_id=station.stationId).dict()
        )
        db_session.add(instrument)
        db_session.commit()

        db_session.add(climsoft_models.Stationelement(
            **climsoft_station_element.get_valid_station_element_input(station_id=station.stationId, instrument_id=instrument.instrumentId, element_id=obs_element.elementId, schedule_class=obs_schedule_class.scheduleClass).dict()
        ))
        db_session.commit()
    db_session.close()


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Stationelement.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                TRUNCATE TABLE {climsoft_models.Obsscheduleclas.__tablename__};
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
                TRUNCATE TABLE {climsoft_models.Stationelement.__tablename__};
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
def get_obs_schedule_class(get_station: climsoft_models.Station):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    obs_schedule_class = climsoft_models.Obsscheduleclas(**climsoft_obsscheduleclass.get_valid_obs_schedule_class_input(station_id=get_station.stationId).dict())
    session.add(obs_schedule_class)
    session.commit()
    yield obs_schedule_class
    session.close()


@pytest.fixture
def get_obselement():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    obselement = climsoft_models.Obselement(**climsoft_obselement.get_valid_obselement_input().dict())
    session.add(obselement)
    session.commit()
    yield obselement
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


@pytest.fixture
def get_station_element(get_station: climsoft_models.Station, get_instrument: climsoft_models.Instrument, get_obselement: climsoft_models.Obselement, get_obs_schedule_class: climsoft_models.Obsscheduleclas):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    station_element = climsoft_models.Stationelement(
        **climsoft_station_element.get_valid_station_element_input(station_id=get_station.stationId, instrument_id=get_instrument.instrumentId, element_id=get_obselement.elementId, schedule_class=get_obs_schedule_class.scheduleClass).dict())
    session.add(station_element)
    session.commit()
    yield station_element
    session.close()


def test_should_return_first_five_station_elements(test_app: TestClient):
    response = test_app.get("/api/v1/climsoft/station-elements", params={"limit": 5})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, stationelement_schema.StationElement)


def test_should_return_single_station_element(test_app: TestClient, get_station_element: climsoft_models.Stationelement):
    response = test_app.get(f"/api/v1/climsoft/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}")
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, stationelement_schema.StationElement)


def test_should_create_a_station_element(test_app: TestClient, get_station: climsoft_models.Station, get_instrument, get_obselement, get_obs_schedule_class):
    station_element_data = climsoft_station_element.get_valid_station_element_input(station_id=get_station.stationId, element_id=get_obselement.elementId, schedule_class=get_obs_schedule_class.scheduleClass, instrument_id=get_instrument.instrumentId).dict(by_alias=True)
    response = test_app.post("/api/v1/climsoft/station-elements", data=json.dumps(station_element_data, default=str))
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, stationelement_schema.StationElement)


def test_should_raise_validation_error(test_app: TestClient, get_station: climsoft_models.Station, get_instrument, get_obselement, get_obs_schedule_class):
    station_element_data = climsoft_station_element.get_valid_station_element_input(station_id=get_station.stationId, element_id=get_obselement.elementId, schedule_class=get_obs_schedule_class.scheduleClass, instrument_id=get_instrument.instrumentId).dict()
    response = test_app.post("/api/v1/climsoft/station-elements", data=json.dumps(station_element_data, default=str))
    assert response.status_code == 422


def test_should_update_station_element(test_app: TestClient, get_station_element: climsoft_models.Stationelement):
    station_element_data = climsoft_station_element.get_valid_station_element_input(station_id=get_station_element.recordedFrom, element_id=get_station_element.describedBy, schedule_class=get_station_element.scheduledFor, instrument_id=get_station_element.recordedWith).dict(by_alias=True)

    recorded_from = station_element_data.pop("recorded_from")
    described_by = station_element_data.pop("described_by")
    recorded_with = station_element_data.pop("recorded_with")
    begin_date = station_element_data.pop("begin_date")

    updates = {**station_element_data, "height": 100}

    response = test_app.put(f"/api/v1/climsoft/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}", data=json.dumps(updates, default=str))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["height"] == updates["height"]


def test_should_delete_station_element(test_app: TestClient, get_station_element: climsoft_models.Stationelement):
    station_element_data = stationelement_schema.StationElement.from_orm(get_station_element).dict(by_alias=True)
    recorded_from = station_element_data.pop("recorded_from")
    described_by = station_element_data.pop("described_by")
    recorded_with = station_element_data.pop("recorded_with")
    begin_date = station_element_data.pop("begin_date")

    response = test_app.delete(f"/api/v1/climsoft/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}")
    assert response.status_code == 200

    response = test_app.get(f"/api/v1/climsoft/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}")
    assert response.status_code == 404

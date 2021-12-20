import datetime
import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from apps.climsoft.db.engine import db_engine
from apps.climsoft.schemas import stationelement_schema
from datagen.climsoft import stationelement as climsoft_station_element, obsscheduleclass as climsoft_obsscheduleclass, obselement as climsoft_obselement, station as climsoft_station, instrument as climsoft_instrument
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
                TRUNCATE TABLE {climsoft_models.Stationelement.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                TRUNCATE TABLE {climsoft_models.Obsscheduleclas.__tablename__};
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
                TRUNCATE TABLE {climsoft_models.Stationelement.__tablename__};
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


def test_should_return_first_five_station_elements(client: TestClient, get_access_token: str):
    response = client.get("/climsoft/v1/station-elements", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, stationelement_schema.StationElement)


def test_should_return_single_station_element(client: TestClient, get_station_element: climsoft_models.Stationelement, get_access_token: str):
    response = client.get(f"/climsoft/v1/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, stationelement_schema.StationElement)


def test_should_create_a_station_element(client: TestClient, get_station: climsoft_models.Station, get_instrument, get_obselement, get_obs_schedule_class, get_access_token: str):
    station_element_data = climsoft_station_element.get_valid_station_element_input(station_id=get_station.stationId, element_id=get_obselement.elementId, schedule_class=get_obs_schedule_class.scheduleClass, instrument_id=get_instrument.instrumentId).dict(by_alias=True)
    response = client.post("/climsoft/v1/station-elements", data=json.dumps(station_element_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, stationelement_schema.StationElement)


def test_should_raise_validation_error(client: TestClient, get_station: climsoft_models.Station, get_instrument, get_obselement, get_obs_schedule_class, get_access_token: str):
    station_element_data = climsoft_station_element.get_valid_station_element_input(station_id=get_station.stationId, element_id=get_obselement.elementId, schedule_class=get_obs_schedule_class.scheduleClass, instrument_id=get_instrument.instrumentId).dict()
    response = client.post("/climsoft/v1/station-elements", data=json.dumps(station_element_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_station_element(client: TestClient, get_station_element: climsoft_models.Stationelement, get_access_token: str):
    station_element_data = climsoft_station_element.get_valid_station_element_input(station_id=get_station_element.recordedFrom, element_id=get_station_element.describedBy, schedule_class=get_station_element.scheduledFor, instrument_id=get_station_element.recordedWith).dict(by_alias=True)

    recorded_from = station_element_data.pop("recorded_from")
    described_by = station_element_data.pop("described_by")
    recorded_with = station_element_data.pop("recorded_with")
    begin_date = station_element_data.pop("begin_date")

    updates = {**station_element_data, "height": 100}

    response = client.put(f"/climsoft/v1/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["height"] == updates["height"]


def test_should_delete_station_element(client: TestClient, get_station_element: climsoft_models.Stationelement, get_access_token: str):
    station_element_data = stationelement_schema.StationElement.from_orm(get_station_element).dict(by_alias=True)
    recorded_from = station_element_data.pop("recorded_from")
    described_by = station_element_data.pop("described_by")
    recorded_with = station_element_data.pop("recorded_with")
    begin_date = station_element_data.pop("begin_date")

    response = client.delete(f"/climsoft/v1/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200

    response = client.get(f"/climsoft/v1/station-elements/{get_station_element.recordedFrom}/{get_station_element.describedBy}/{get_station_element.recordedWith}/{get_station_element.beginDate}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 404

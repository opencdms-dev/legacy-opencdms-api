import datetime
import json
import uuid

import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from apps.climsoft.db.engine import db_engine
from apps.climsoft.schemas import faultresolution_schema
from datagen.climsoft import faultresolution as climsoft_fault_resolution, \
    instrumentfaultreport as climsoft_instrument_fault_report, station as climsoft_station, \
    instrument as climsoft_instrument
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
                TRUNCATE TABLE {climsoft_models.Faultresolution.__tablename__};
                TRUNCATE TABLE {climsoft_models.Instrumentfaultreport.__tablename__};
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

        instrument = climsoft_models.Instrument(
            **climsoft_instrument.get_valid_instrument_input(station_id=station.stationId).dict()
        )
        db_session.add(instrument)
        db_session.commit()

        instrument_fault_report = climsoft_models.Instrumentfaultreport(
            **climsoft_instrument_fault_report.get_valid_instrument_fault_report_input(station_id=station.stationId,
                                                                                       instrument_id=instrument.instrumentId).dict()
        )
        db_session.add(instrument_fault_report)
        db_session.commit()

        db_session.add(climsoft_models.Faultresolution(
            **climsoft_fault_resolution.get_valid_fault_resolution_input(
                instrument_fault_report_id=instrument_fault_report.reportId
            ).dict()
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
                TRUNCATE TABLE {climsoft_models.Faultresolution.__tablename__};
                TRUNCATE TABLE {climsoft_models.Instrumentfaultreport.__tablename__};
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
def get_instrument(get_station: climsoft_models.Station):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    instrument = climsoft_models.Instrument(
        **climsoft_instrument.get_valid_instrument_input(station_id=get_station.stationId).dict())
    session.add(instrument)
    session.commit()
    yield instrument
    session.close()


@pytest.fixture
def get_instrument_fault_report(get_station: climsoft_models.Station, get_instrument: climsoft_models.Instrument):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    instrument_fault_report = climsoft_models.Instrumentfaultreport(
        **climsoft_instrument_fault_report.get_valid_instrument_fault_report_input(
            station_id=get_station.stationId,
            instrument_id=get_instrument.instrumentId
        ).dict()
    )
    session.add(instrument_fault_report)
    session.commit()

    yield instrument_fault_report
    session.close()


@pytest.fixture
def get_fault_resolution(get_instrument_fault_report):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    fault_resolution = climsoft_models.Faultresolution(
        **climsoft_fault_resolution.get_valid_fault_resolution_input(
            instrument_fault_report_id=get_instrument_fault_report.reportId
        ).dict()
    )
    session.add(fault_resolution)
    session.commit()
    yield fault_resolution
    session.close()


def test_should_return_first_five_station_location_histories(client: TestClient, get_access_token: str):
    response = client.get("/climsoft/v1/fault-resolutions", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5


def test_should_return_single_fault_resolution(
    client: TestClient,
    get_fault_resolution: climsoft_models.Faultresolution,
    get_access_token: str
):
    response = client.get(
        f"/climsoft/v1/fault-resolutions/{get_fault_resolution.resolvedDatetime}/{get_fault_resolution.associatedWith}",
        headers={
            "Authorization": f"Bearer {get_access_token}"
        }
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1


def test_should_create_a_fault_resolution(
        client: TestClient,
        get_instrument_fault_report: climsoft_models.Instrumentfaultreport,
        get_access_token: str
):
    fault_resolution_data = climsoft_fault_resolution.get_valid_fault_resolution_input(
        instrument_fault_report_id=get_instrument_fault_report.reportId
    ).dict(by_alias=True)
    response = client.post(
        "/climsoft/v1/fault-resolutions",
        data=json.dumps(fault_resolution_data, default=str), headers={
            "Authorization": f"Bearer {get_access_token}"
        }
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1


def test_should_raise_validation_error(client: TestClient,
                                       get_instrument_fault_report: climsoft_models.Instrumentfaultreport, 
                                       get_access_token: str):
    fault_resolution_data = climsoft_fault_resolution.get_valid_fault_resolution_input(
        instrument_fault_report_id=get_instrument_fault_report.reportId
    ).dict()
    response = client.post(
        "/climsoft/v1/fault-resolutions",
        data=json.dumps(fault_resolution_data, default=str), headers={
            "Authorization": f"Bearer {get_access_token}"
        }
    )
    assert response.status_code == 422


def test_should_update_fault_resolution(
    client: TestClient,
    get_fault_resolution: climsoft_models.Faultresolution,
    get_access_token: str
):
    fault_resolution_data = faultresolution_schema.FaultResolution.from_orm(
        get_fault_resolution
    ).dict(by_alias=True)

    resolved_datetime = fault_resolution_data.pop("resolved_datetime")
    associated_with = fault_resolution_data.pop("associated_with")

    updates = {**fault_resolution_data, "remarks": uuid.uuid4().hex}

    response = client.put(
        f"/climsoft/v1/fault-resolutions/{resolved_datetime}/{associated_with}",
        data=json.dumps(updates, default=str), headers={
            "Authorization": f"Bearer {get_access_token}"
        }
    )
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["remarks"] == updates["remarks"]


def test_should_delete_fault_resolution(
        client: TestClient,
        get_fault_resolution,
        get_access_token: str
):
    fault_resolution_data = faultresolution_schema.FaultResolution.from_orm(
        get_fault_resolution).dict(by_alias=True)

    resolved_datetime = fault_resolution_data.pop("resolved_datetime")
    associated_with = fault_resolution_data.pop("associated_with")

    response = client.delete(
        f"/climsoft/v1/fault-resolutions/{resolved_datetime}/{associated_with}",
        headers={
            "Authorization": f"Bearer {get_access_token}"
        }
    )
    assert response.status_code == 200

    response = client.get(f"/climsoft/v1/fault-resolutions/{resolved_datetime}/{associated_with}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })

    assert response.status_code == 404

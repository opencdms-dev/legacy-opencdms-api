import datetime
import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.apps.climsoft.db.engine import db_engine
from src.apps.climsoft.schemas import observationinitial_schema
from tests.datagen.climsoft import observationinitial as climsoft_observation_initial, obsscheduleclass as climsoft_obsscheduleclass, obselement as climsoft_obselement, station as climsoft_station, instrument as climsoft_instrument
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Observationinitial.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
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

        db_session.add(climsoft_models.Observationinitial(
            **climsoft_observation_initial.get_valid_observation_initial_input(station_id=station.stationId, element_id=obs_element.elementId).dict()
        ))
        db_session.commit()
    db_session.close()


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Observationinitial.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
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
def get_obselement():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    obselement = climsoft_models.Obselement(**climsoft_obselement.get_valid_obselement_input().dict())
    session.add(obselement)
    session.commit()
    yield obselement
    session.close()


@pytest.fixture
def get_observation_initial(get_station: climsoft_models.Station, get_obselement: climsoft_models.Obselement):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    observation_initial = climsoft_models.Observationinitial(
        **climsoft_observation_initial.get_valid_observation_initial_input(station_id=get_station.stationId, element_id=get_obselement.elementId).dict())
    session.add(observation_initial)
    session.commit()
    yield observation_initial
    session.close()


def test_should_return_first_five_observation_initials(test_app: TestClient):
    response = test_app.get("/api/v1/climsoft/observation-initials", params={"limit": 5})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, observationinitial_schema.ObservationInitial)


def test_should_return_single_observation_initial(test_app: TestClient, get_observation_initial: climsoft_models.Observationinitial):
    response = test_app.get(f"/api/v1/climsoft/observation-initials/{get_observation_initial.recordedFrom}/{get_observation_initial.describedBy}/{get_observation_initial.obsDatetime}/{get_observation_initial.qcStatus}/{get_observation_initial.acquisitionType}")
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, observationinitial_schema.ObservationInitial)


def test_should_create_a_observation_initial(test_app: TestClient, get_station: climsoft_models.Station, get_obselement: climsoft_models.Obselement):
    observation_initial_data = climsoft_observation_initial.get_valid_observation_initial_input(station_id=get_station.stationId, element_id=get_obselement.elementId).dict(by_alias=True)
    response = test_app.post("/api/v1/climsoft/observation-initials", data=json.dumps(observation_initial_data, default=lambda x: x.strftime("%Y-%m-%d %H:%M:%S")))
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, observationinitial_schema.ObservationInitial)


def test_should_raise_validation_error(test_app: TestClient, get_station: climsoft_models.Station, get_obselement: climsoft_models.Obselement):
    observation_initial_data = climsoft_observation_initial.get_valid_observation_initial_input(station_id=get_station.stationId, element_id=get_obselement.elementId).dict()
    response = test_app.post("/api/v1/climsoft/observation-initials", data=json.dumps(observation_initial_data, default=str))
    assert response.status_code == 422


def test_should_update_observation_initial(test_app: TestClient, get_observation_initial: climsoft_models.Observationinitial):
    observation_initial_data = climsoft_observation_initial.get_valid_observation_initial_input(station_id=get_observation_initial.recordedFrom, element_id=get_observation_initial.describedBy, obs_datetime=str(get_observation_initial.obsDatetime), qc_status=get_observation_initial.qcStatus, acquisition_type=get_observation_initial.acquisitionType).dict(by_alias=True)

    recorded_from = observation_initial_data.pop("recorded_from")
    described_by = observation_initial_data.pop("described_by")
    obs_datetime = observation_initial_data.pop("obs_datetime")
    qc_status = observation_initial_data.pop("qc_status")
    acquisition_type = observation_initial_data.pop("acquisition_type")

    updates = {**observation_initial_data, "period": 100}

    response = test_app.put(f"/api/v1/climsoft/observation-initials/{get_observation_initial.recordedFrom}/{get_observation_initial.describedBy}/{get_observation_initial.obsDatetime}/{get_observation_initial.qcStatus}/{get_observation_initial.acquisitionType}", data=json.dumps(updates, default=str))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["period"] == updates["period"]


def test_should_delete_observation_initial(test_app: TestClient, get_observation_initial: climsoft_models.Observationinitial):
    observation_initial_data = observationinitial_schema.ObservationInitial.from_orm(get_observation_initial).dict(by_alias=True)

    recorded_from = observation_initial_data.pop("recorded_from")
    described_by = observation_initial_data.pop("described_by")
    obs_datetime = observation_initial_data.pop("obs_datetime")
    qc_status = observation_initial_data.pop("qc_status")
    acquisition_type = observation_initial_data.pop("acquisition_type")

    response = test_app.delete(f"/api/v1/climsoft/observation-initials/{get_observation_initial.recordedFrom}/{get_observation_initial.describedBy}/{get_observation_initial.obsDatetime}/{get_observation_initial.qcStatus}/{get_observation_initial.acquisitionType}")
    assert response.status_code == 200

    response = test_app.get(f"/api/v1/climsoft/observation-initials/{get_observation_initial.recordedFrom}/{get_observation_initial.describedBy}/{get_observation_initial.obsDatetime}/{get_observation_initial.qcStatus}/{get_observation_initial.acquisitionType}")
    assert response.status_code == 404

import datetime
import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.apps.climsoft.db.engine import db_engine
from src.apps.climsoft.schemas import observationfinal_schema
from tests.datagen.climsoft import observationfinal as climsoft_observation_final, obsscheduleclass as climsoft_obsscheduleclass, obselement as climsoft_obselement, station as climsoft_station, instrument as climsoft_instrument
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Observationfinal.__tablename__};
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

        db_session.add(climsoft_models.Observationfinal(
            **climsoft_observation_final.get_valid_observation_final_input(station_id=station.stationId, element_id=obs_element.elementId).dict()
        ))
        db_session.commit()
    db_session.close()


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Observationfinal.__tablename__};
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
def get_observation_final(get_station: climsoft_models.Station, get_obselement: climsoft_models.Obselement):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    observation_final = climsoft_models.Observationfinal(
        **climsoft_observation_final.get_valid_observation_final_input(station_id=get_station.stationId, element_id=get_obselement.elementId).dict())
    session.add(observation_final)
    session.commit()
    yield observation_final
    session.close()


def test_should_return_first_five_observation_finals(test_app: TestClient):
    response = test_app.get("/api/v1/climsoft/observation-finals", params={"limit": 5})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, observationfinal_schema.ObservationFinal)


def test_should_return_single_observation_final(test_app: TestClient, get_observation_final: climsoft_models.Observationfinal):
    response = test_app.get(f"/api/v1/climsoft/observation-finals/{get_observation_final.recordedFrom}/{get_observation_final.describedBy}/{get_observation_final.obsDatetime}")
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, observationfinal_schema.ObservationFinal)


def test_should_create_a_observation_final(test_app: TestClient, get_station: climsoft_models.Station, get_obselement: climsoft_models.Obselement):
    observation_final_data = climsoft_observation_final.get_valid_observation_final_input(station_id=get_station.stationId, element_id=get_obselement.elementId).dict(by_alias=True)
    response = test_app.post("/api/v1/climsoft/observation-finals", data=json.dumps(observation_final_data, default=lambda x: x.strftime("%Y-%m-%d %H:%M:%S")))
    assert response.status_code == 200
    response_data = response.json()
    print(response_data)
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, observationfinal_schema.ObservationFinal)


def test_should_raise_validation_error(test_app: TestClient, get_station: climsoft_models.Station, get_obselement: climsoft_models.Obselement):
    observation_final_data = climsoft_observation_final.get_valid_observation_final_input(station_id=get_station.stationId, element_id=get_obselement.elementId).dict()
    response = test_app.post("/api/v1/climsoft/observation-finals", data=json.dumps(observation_final_data, default=str))
    assert response.status_code == 422


def test_should_update_observation_final(test_app: TestClient, get_observation_final: climsoft_models.Observationfinal):
    observation_final_data = climsoft_observation_final.get_valid_observation_final_input(station_id=get_observation_final.recordedFrom, element_id=get_observation_final.describedBy, obs_datetime=str(get_observation_final.obsDatetime), qc_status=get_observation_final.qcStatus, acquisition_type=get_observation_final.acquisitionType).dict(by_alias=True)

    recorded_from = observation_final_data.pop("recorded_from")
    described_by = observation_final_data.pop("described_by")
    obs_datetime = observation_final_data.pop("obs_datetime")

    updates = {**observation_final_data, "period": 100}

    response = test_app.put(f"/api/v1/climsoft/observation-finals/{get_observation_final.recordedFrom}/{get_observation_final.describedBy}/{get_observation_final.obsDatetime}", data=json.dumps(updates, default=str))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["period"] == updates["period"]


def test_should_delete_observation_final(test_app: TestClient, get_observation_final: climsoft_models.Observationfinal):
    observation_final_data = observationfinal_schema.ObservationFinal.from_orm(get_observation_final).dict(by_alias=True)

    recorded_from = observation_final_data.pop("recorded_from")
    described_by = observation_final_data.pop("described_by")
    obs_datetime = observation_final_data.pop("obs_datetime")

    response = test_app.delete(f"/api/v1/climsoft/observation-finals/{get_observation_final.recordedFrom}/{get_observation_final.describedBy}/{get_observation_final.obsDatetime}")
    assert response.status_code == 200

    response = test_app.get(f"/api/v1/climsoft/observation-finals/{get_observation_final.recordedFrom}/{get_observation_final.describedBy}/{get_observation_final.obsDatetime}")
    assert response.status_code == 404

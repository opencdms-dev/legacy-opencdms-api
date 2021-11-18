import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.apps.climsoft.db.engine import db_engine
from src.apps.climsoft.schemas import obsscheduleclass_schema
from tests.datagen.climsoft import obsscheduleclass as climsoft_obs_schedule_class, station as climsoft_station
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Obsscheduleclas.__tablename__};
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

        db_session.add(climsoft_models.Obsscheduleclas(
            **climsoft_obs_schedule_class.get_valid_obs_schedule_class_input(station_id=station.stationId).dict()
        ))
        db_session.commit()
    db_session.close()


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Obsscheduleclas.__tablename__};
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
def get_obs_schedule_class(get_station: climsoft_models.Station):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    obs_schedule_class = climsoft_models.Obsscheduleclas(**climsoft_obs_schedule_class.get_valid_obs_schedule_class_input(station_id=get_station.stationId).dict())
    session.add(obs_schedule_class)
    session.commit()
    yield obs_schedule_class
    session.close()


def test_should_return_first_five_obs_schedule_classs(test_app: TestClient):
    response = test_app.get("/api/v1/climsoft/obs-schedule-class", params={"limit": 5})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, obsscheduleclass_schema.ObsScheduleClass)


def test_should_return_single_obs_schedule_class(test_app: TestClient, get_obs_schedule_class: climsoft_models.Obsscheduleclas):
    response = test_app.get(f"/api/v1/climsoft/obs-schedule-class/{get_obs_schedule_class.scheduleClass}")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, obsscheduleclass_schema.ObsScheduleClass)


def test_should_create_a_obs_schedule_class(test_app: TestClient, get_station: climsoft_models.Station):
    obs_schedule_class_data = climsoft_obs_schedule_class.get_valid_obs_schedule_class_input(station_id=get_station.stationId).dict(by_alias=True)
    response = test_app.post("/api/v1/climsoft/obs-schedule-class", data=json.dumps(obs_schedule_class_data, default=str))
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, obsscheduleclass_schema.ObsScheduleClass)


def test_should_raise_validation_error(test_app: TestClient, get_station: climsoft_models.Station):
    obs_schedule_class_data = climsoft_obs_schedule_class.get_valid_obs_schedule_class_input(station_id=get_station.stationId).dict()
    response = test_app.post("/api/v1/climsoft/obs-schedule-class", data=json.dumps(obs_schedule_class_data, default=str))
    assert response.status_code == 422


def test_should_update_obs_schedule_class(test_app: TestClient, get_obs_schedule_class: climsoft_models.Obsscheduleclas):
    obs_schedule_class_data = obsscheduleclass_schema.ObsScheduleClass.from_orm(get_obs_schedule_class).dict(by_alias=True)
    obs_schedule_class_id = obs_schedule_class_data.pop("schedule_class")
    updates = {**obs_schedule_class_data, "description": "updated description"}

    response = test_app.put(f"/api/v1/climsoft/obs-schedule-class/{obs_schedule_class_id}", data=json.dumps(updates, default=str))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["description"] == updates["description"]


def test_should_delete_obs_schedule_class(test_app: TestClient, get_obs_schedule_class):
    obs_schedule_class_data = obsscheduleclass_schema.ObsScheduleClass.from_orm(get_obs_schedule_class).dict(by_alias=True)
    obs_schedule_class_id = obs_schedule_class_data.pop("schedule_class")

    response = test_app.delete(f"/api/v1/climsoft/obs-schedule-class/{obs_schedule_class_id}")
    assert response.status_code == 200

    response = test_app.get(f"/api/v1/climsoft/obs-schedule-class/{obs_schedule_class_id}")
    assert response.status_code == 404

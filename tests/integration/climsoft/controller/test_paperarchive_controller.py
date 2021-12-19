import datetime
import json
import uuid

import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from apps.climsoft.db.engine import db_engine
from apps.climsoft.schemas import paperarchive_schema
from datagen.climsoft import (
    paperarchive as climsoft_paper_archive,
    paperarchivedefinition as climsoft_paper_archive_definition,
    station as climsoft_station
)
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
                TRUNCATE TABLE {climsoft_models.Paperarchive.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                TRUNCATE TABLE {climsoft_models.Paperarchivedefinition.__tablename__};
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

        paper_archive_definition = climsoft_models.Paperarchivedefinition(
            **climsoft_paper_archive_definition.get_valid_paper_archive_definition_input().dict()
        )
        db_session.add(paper_archive_definition)
        db_session.commit()

        db_session.add(climsoft_models.Paperarchive(
            **climsoft_paper_archive.get_valid_paper_archive_input(
                station_id=station.stationId,
                paper_archive_definition_id=paper_archive_definition.formId
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
                TRUNCATE TABLE {climsoft_models.Paperarchive.__tablename__};
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                TRUNCATE TABLE {climsoft_models.Paperarchivedefinition.__tablename__};
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
def get_paper_archive_definition():
    Session = sessionmaker(bind=db_engine)
    session = Session()

    paper_archive_definition = climsoft_models.Paperarchivedefinition(
        **climsoft_paper_archive_definition.get_valid_paper_archive_definition_input().dict()
    )
    session.add(paper_archive_definition)
    session.commit()
    yield paper_archive_definition
    session.close()


@pytest.fixture
def get_paper_archive():
    Session = sessionmaker(bind=db_engine)
    session = Session()

    station = climsoft_models.Station(**climsoft_station.get_valid_station_input().dict())
    session.add(station)
    session.commit()

    paper_archive_definition = climsoft_models.Paperarchivedefinition(
        **climsoft_paper_archive_definition.get_valid_paper_archive_definition_input().dict()
    )
    session.add(paper_archive_definition)
    session.commit()
    paper_archive_data = climsoft_paper_archive.get_valid_paper_archive_input(
        station_id=station.stationId,
        paper_archive_definition_id=paper_archive_definition.formId
    ).dict()
    paper_archive = climsoft_models.Paperarchive(
        **paper_archive_data
    )
    session.add(paper_archive)
    session.commit()
    yield paper_archive
    session.close()


def test_should_return_first_five_paper_archives(client: TestClient, get_access_token: str):
    response = client.get("/climsoft/v1/paper-archives", params={"limit": 5}, headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, paperarchive_schema.PaperArchive)


def test_should_return_single_paper_archive(client: TestClient, get_paper_archive: climsoft_models.Paperarchive, get_access_token: str):
    print(get_paper_archive.belongsTo)
    response = client.get(f"/climsoft/v1/paper-archives/{get_paper_archive.belongsTo}/{get_paper_archive.formDatetime}/{get_paper_archive.classifiedInto}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    print(response.json())
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, paperarchive_schema.PaperArchive)


def test_should_create_a_paper_archive(client: TestClient, get_station: climsoft_models.Station, get_paper_archive_definition: climsoft_models.Paperarchivedefinition, get_access_token: str):
    paper_archive_data = climsoft_paper_archive.get_valid_paper_archive_input(station_id=get_station.stationId, paper_archive_definition_id=get_paper_archive_definition.formId).dict(by_alias=True)
    response = client.post("/climsoft/v1/paper-archives", data=json.dumps(paper_archive_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, paperarchive_schema.PaperArchive)


def test_should_raise_validation_error(client: TestClient, get_station: climsoft_models.Station, get_paper_archive_definition: climsoft_models.Paperarchivedefinition, get_access_token: str):
    paper_archive_data = climsoft_paper_archive.get_valid_paper_archive_input(station_id=get_station.stationId, paper_archive_definition_id=get_paper_archive_definition.formId).dict()
    response = client.post("/climsoft/v1/paper-archives", data=json.dumps(paper_archive_data, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 422


def test_should_update_paper_archive(client: TestClient, get_paper_archive: climsoft_models.Paperarchive, get_access_token: str):
    paper_archive_data = climsoft_paper_archive.get_valid_paper_archive_input(station_id=get_paper_archive.belongsTo, paper_archive_definition_id=get_paper_archive.classifiedInto).dict(by_alias=True)

    belongs_to = paper_archive_data.pop("belongs_to")
    classified_into = paper_archive_data.pop("classified_into")
    form_datetime = paper_archive_data.pop("form_datetime")

    updates = {**paper_archive_data, "image": uuid.uuid4().hex}

    response = client.put(f"/climsoft/v1/paper-archives/{get_paper_archive.belongsTo}/{get_paper_archive.formDatetime}/{get_paper_archive.classifiedInto}", data=json.dumps(updates, default=str), headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["image"] == updates["image"]


def test_should_delete_paper_archive(client: TestClient, get_paper_archive: climsoft_models.Paperarchive, get_access_token: str):
    paper_archive_data = paperarchive_schema.PaperArchive.from_orm(get_paper_archive).dict(by_alias=True)
    print(paper_archive_data)
    belongs_to = paper_archive_data.pop("belongs_to")
    classified_into = paper_archive_data.pop("classified_into")
    form_datetime = paper_archive_data.pop("form_datetime")

    response = client.delete(f"/climsoft/v1/paper-archives/{get_paper_archive.belongsTo}/{get_paper_archive.formDatetime}/{get_paper_archive.classifiedInto}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    print(response.json())
    assert response.status_code == 200

    response = client.get(f"/climsoft/v1/paper-archives/{get_paper_archive.belongsTo}/{get_paper_archive.formDatetime}/{get_paper_archive.classifiedInto}", headers={
        "Authorization": f"Bearer {get_access_token}"
    })
    assert response.status_code == 404

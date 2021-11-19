import json
import pytest
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm.session import sessionmaker
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.apps.climsoft.db.engine import db_engine
from src.apps.climsoft.schemas import obselement_schema
from tests.datagen.climsoft import obselement as climsoft_obselement
from faker import Faker
from fastapi.testclient import TestClient

fake = Faker()


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))

    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    for i in range(1, 11):
        db_session.add(climsoft_models.Obselement(
            **climsoft_obselement.get_valid_obselement_input().dict()
        ))
    db_session.commit()
    db_session.close()


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Obselement.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))


@pytest.fixture
def get_obselement():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    obselement = climsoft_models.Obselement(**climsoft_obselement.get_valid_obselement_input().dict())
    session.add(obselement)
    session.commit()
    yield obselement
    session.close()


def test_should_return_first_five_obselements(test_app: TestClient):
    response = test_app.get("/api/climsoft/v1/obselements", params={"limit": 5})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 5
    for s in response_data["result"]:
        isinstance(s, obselement_schema.ObsElement)


def test_should_return_single_station(test_app: TestClient, get_obselement: climsoft_models.Obselement):
    response = test_app.get(f"/api/climsoft/v1/obselements/{get_obselement.elementId}")

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, obselement_schema.ObsElement)


def test_should_create_a_station(test_app: TestClient):
    obselement_data = climsoft_obselement.get_valid_obselement_input().dict(by_alias=True)
    response = test_app.post("/api/climsoft/v1/obselements", data=json.dumps(obselement_data, default=str))
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["result"]) == 1
    for s in response_data["result"]:
        isinstance(s, obselement_schema.ObsElement)


def test_should_raise_validation_error(test_app: TestClient):
    obselement_data = climsoft_obselement.get_valid_obselement_input().dict()
    response = test_app.post("/api/climsoft/v1/obselements", data=json.dumps(obselement_data, default=str))
    assert response.status_code == 422


def test_should_update_station(test_app: TestClient, get_obselement):
    obselement_data = obselement_schema.ObsElement.from_orm(get_obselement).dict(by_alias=True)
    element_id = obselement_data.pop("element_id")
    updates = {**obselement_data, "element_name": "updated name"}
    response = test_app.put(f"/api/climsoft/v1/obselements/{element_id}", data=json.dumps(updates, default=str))
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["result"][0]["element_name"] == updates["element_name"]


def test_should_delete_station(test_app: TestClient, get_obselement):
    obselement_data = obselement_schema.ObsElement.from_orm(get_obselement).dict(by_alias=True)
    element_id = obselement_data.pop("element_id")

    response = test_app.delete(f"/api/climsoft/v1/obselements/{element_id}")
    assert response.status_code == 200

    response = test_app.get(f"/api/climsoft/v1/obselements/{element_id}")

    assert response.status_code == 404

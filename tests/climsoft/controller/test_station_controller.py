import datetime
import random
import uuid
from typing import Tuple
from sqlalchemy.sql import text as sa_text
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from fastapi_sqlalchemy import db
from db.engine import db_engine
from apps.climsoft.schemas import station_schema
from faker import Faker

fake = Faker()


def get_valid_station_input():
    # lat, lng, city, country, timezone
    location: Tuple[str, str, str, str, str] = fake.local_latlng()
    return station_schema.Station(
        stationId=uuid.uuid4().hex,
        stationName=uuid.uuid4().hex,
        wmoid=uuid.uuid4().hex[:20],
        icaoid=uuid.uuid4().hex[:20],
        latitude=float(location[0]),
        longitude=float(location[1]),
        elevation=str(random.randint(0, 45)),
        geoLocationMethod=uuid.uuid4().hex,
        geoLocationAccuracy=random.random(),
        openingDatetime=datetime.datetime.now(),
        closingDatetime=datetime.datetime.now()+datetime.timedelta(days=999),
        country=location[3],
        authority=uuid.uuid4().hex,
        adminRegion=location[3],
        drainageBasin=uuid.uuid4().hex,
        wacaSelection=True,
        cptSelection=True,
        stationOperational=True,
        qualifier=uuid.uuid4().hex[:20]
    )


def setup_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))
    db_session = db.session
    for i in range(1, 11):
        db_session.add(climsoft_models.Station(
            **get_valid_station_input().dict()
        ))
    db_session.commit()


def teardown_module(module):
    with db_engine.connect().execution_options(autocommit=True) as connection:
        with connection.begin():
            db_engine.execute(sa_text(f"""
                SET FOREIGN_KEY_CHECKS = 0;
                TRUNCATE TABLE {climsoft_models.Station.__tablename__};
                SET FOREIGN_KEY_CHECKS = 1;
            """))

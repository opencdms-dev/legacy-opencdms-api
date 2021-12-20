import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import stationlocationhistory_schema


fake = Faker()


def get_valid_station_location_history_input(station_id: str):
    return stationlocationhistory_schema.StationLocationHistory(
        belongsTo=station_id,
        stationType=uuid.uuid4().hex,
        latitude=fake.latitude(),
        longitude=fake.longitude(),
        geoLocationMethod=uuid.uuid4().hex,
        geoLocationAccuracy=random.random(),
        openingDatetime=datetime.datetime.utcnow(),
        closingDatetime=datetime.datetime.utcnow(),
        elevation=random.randint(10, 80),
        authority=uuid.uuid4().hex,
        adminRegion=uuid.uuid4().hex,
        drainageBasin=uuid.uuid4().hex
    )

import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import station_schema


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
        openingDatetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        closingDatetime=(datetime.datetime.now() + datetime.timedelta(days=999)).strftime("%Y-%m-%d %H:%M:%S"),
        country=location[3],
        authority=uuid.uuid4().hex,
        adminRegion=location[3],
        drainageBasin=uuid.uuid4().hex,
        wacaSelection=True,
        cptSelection=True,
        stationOperational=True,
        qualifier=uuid.uuid4().hex[:20]
    )

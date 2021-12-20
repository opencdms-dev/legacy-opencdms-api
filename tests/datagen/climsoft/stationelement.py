import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import stationelement_schema


fake = Faker()


def get_valid_station_element_input(station_id: str, instrument_id: str, element_id: int, schedule_class: str):
    return stationelement_schema.StationElement(
        recordedFrom=station_id,
        recordedWith=instrument_id,
        describedBy=element_id,
        instrumentcode=uuid.uuid4().hex[:6],
        scheduledFor=schedule_class,
        height=random.random()*100000,
        beginDate=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        endDate=(datetime.datetime.utcnow()+datetime.timedelta(days=1234)).strftime("%Y-%m-%dT%H:%M:%SZ")
    )

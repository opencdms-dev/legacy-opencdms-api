import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import observationfinal_schema


fake = Faker()


def get_valid_observation_final_input(station_id: str, element_id: int, obs_datetime: str = None, qc_status: int = None, acquisition_type: int = None):
    return observationfinal_schema.ObservationFinalInputGen(
        recordedFrom=station_id,
        describedBy=element_id,
        obsDatetime=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") if obs_datetime is None else obs_datetime,
        qcStatus=random.randint(1, 10) if qc_status is None else qc_status,
        acquisitionType=random.randint(1, 10) if acquisition_type is None else acquisition_type,
        obsLevel=uuid.uuid4().hex,
        obsValue=uuid.uuid4().hex,
        flag=uuid.uuid4().hex,
        period=random.choice([10, 100, 1000]),
        qcTypeLog=fake.sentence(),
        dataForm=uuid.uuid4().hex,
        capturedBy=uuid.uuid4().hex,
        mark=True,
        temperatureUnits=uuid.uuid4().hex,
        precipitationUnits=uuid.uuid4().hex,
        cloudHeightUnits=uuid.uuid4().hex,
        visUnits=uuid.uuid4().hex,
        dataSourceTimeZone=random.randint(1, 180)
    )

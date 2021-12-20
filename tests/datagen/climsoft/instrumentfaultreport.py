import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import instrumentfaultreport_schema


fake = Faker()


def get_valid_instrument_fault_report_input(station_id: str, instrument_id: str):
    return instrumentfaultreport_schema.InstrumentFaultReport(
        refersTo=instrument_id,
        reportId=random.randint(10000, 1000000),
        reportDatetime=datetime.datetime.utcnow(),
        faultDescription=" ".join(fake.sentences()),
        reportedBy=uuid.uuid4().hex,
        receivedDatetime=datetime.datetime.utcnow(),
        receivedBy=uuid.uuid4().hex,
        reportedFrom=station_id
    )

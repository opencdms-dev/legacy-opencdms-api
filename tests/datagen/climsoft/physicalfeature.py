import uuid
import datetime
from faker import Faker
from apps.climsoft.schemas import physicalfeature_schema


fake = Faker()


def get_valid_physical_feature_input(station_id: str, feature_class: str):
    return physicalfeature_schema.PhysicalFeature(
        associatedWith=station_id,
        beginDate=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        endDate=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        image=uuid.uuid4().hex,
        description=fake.sentence(),
        classifiedInto=feature_class
    )

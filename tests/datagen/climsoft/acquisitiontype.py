import random
from faker import Faker
from apps.climsoft.schemas import acquisitiontype_schema

fake = Faker()


def get_valid_acquisition_type_input():
    return acquisitiontype_schema.CreateAcquisitionType(
        code=random.randint(10000000, 99999999),
        description=fake.sentence()
    )

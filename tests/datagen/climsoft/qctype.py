import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import qctype_schema


fake = Faker()


def get_valid_qc_type_input():
    return qctype_schema.QCType(
        code=random.randint(1000000, 10000000),
        description=" ".join(fake.sentences())
    )

import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import regkey_schema


fake = Faker()


def get_valid_reg_key_input():
    return regkey_schema.RegKey(
        keyName=uuid.uuid4().hex,
        keyValue=uuid.uuid4().hex,
        keyDescription=" ".join(fake.sentences())
    )

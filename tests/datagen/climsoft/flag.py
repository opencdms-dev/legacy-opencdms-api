import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import flag_schema


fake = Faker()


def get_valid_flag_input():
    return flag_schema.Flag(
        characterSymbol=uuid.uuid4().hex,
        numSymbol=random.randint(1000000, 10000000),
        description=" ".join(fake.sentences())
    )

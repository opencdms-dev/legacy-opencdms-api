import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from src.apps.climsoft.schemas import qcstatusdefinition_schema


fake = Faker()


def get_valid_paper_archive_definition_input():
    return qcstatusdefinition_schema.QCStatusDefinition(
        code=random.randint(1000000, 10000000),
        description=" ".join(fake.sentences())
    )

import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import synopfeature_schema


fake = Faker()


def get_valid_synop_feature_input():
    return synopfeature_schema.SynopFeature(
        abbreviation=uuid.uuid4().hex,
        description=" ".join(fake.sentences())
    )

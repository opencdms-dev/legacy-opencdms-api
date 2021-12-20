import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import featuregeographicalposition_schema


fake = Faker()


def get_valid_feature_geographical_position_input(synop_feature_abbreviation: str):
    return featuregeographicalposition_schema.FeatureGeographicalPosition(
        belongsTo=synop_feature_abbreviation,
        observedOn=datetime.datetime.utcnow().isoformat(),
        latitude=fake.latitude(),
        longitude=fake.longitude()
    )

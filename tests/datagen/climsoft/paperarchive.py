import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import paperarchive_schema


fake = Faker()


def get_valid_paper_archive_input(station_id: str, paper_archive_definition_id: str):
    return paperarchive_schema.CreatePaperArchive(**dict(
        belongs_to=station_id,
        form_datetime=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        image=uuid.uuid4().hex,
        classified_into=paper_archive_definition_id
    ))

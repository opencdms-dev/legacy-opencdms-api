import uuid
import random
import datetime
from typing import Tuple
from faker import Faker
from apps.climsoft.schemas import paperarchivedefinition_schema


fake = Faker()


def get_valid_paper_archive_definition_input():
    return paperarchivedefinition_schema.PaperArchiveDefinition(
        formId=uuid.uuid4().hex,
        description=" ".join(fake.sentences())
    )

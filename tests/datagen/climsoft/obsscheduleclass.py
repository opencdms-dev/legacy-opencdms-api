import uuid
from faker import Faker
from apps.climsoft.schemas import obsscheduleclass_schema


fake = Faker()


def get_valid_obs_schedule_class_input(station_id: str):
    return obsscheduleclass_schema.ObsScheduleClass(
        scheduleClass=uuid.uuid4().hex,
        description=uuid.uuid4().hex,
        refersTo=station_id
    )

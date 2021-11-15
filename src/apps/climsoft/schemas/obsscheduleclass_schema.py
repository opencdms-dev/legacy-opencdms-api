from typing import List
from pydantic import BaseModel, constr
from src.apps.climsoft.schemas import Response, station_schema

field_names = {
    "scheduleClass": "schedule_class",
    "refersTo": "refers_to"
}


class CreateObsScheduleClass(BaseModel):
    scheduleClass: constr(max_length=255)
    description: constr(max_length=255)
    refersTo: constr(max_length=255)

    class Config:
        fields = field_names


class UpdateObsScheduleClass(CreateObsScheduleClass):
    pass


class ObsScheduleClass(CreateObsScheduleClass):
    pass


class ObsScheduleClassResponse(Response):
    result: List[ObsScheduleClass]


class ObsScheduleClassWithStation(ObsScheduleClass):
    station: station_schema.Station


class ObsScheduleClassWithStationResponse(Response):
    result: List[ObsScheduleClassWithStation]




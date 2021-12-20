from typing import List
from pydantic import BaseModel, constr
from apps.climsoft.schemas import Response, station_schema

field_names = {
    "refersTo": "refers_to"
}


class CreateObsScheduleClass(BaseModel):
    scheduleClass: constr(max_length=255)
    description: constr(max_length=255)
    refersTo: constr(max_length=255)

    class Config:
        fields = {**field_names, "scheduleClass": "schedule_class"}


class UpdateObsScheduleClass(BaseModel):
    description: constr(max_length=255)
    refersTo: constr(max_length=255)

    class Config:
        fields = field_names


class ObsScheduleClass(CreateObsScheduleClass):

    class Config:
        fields = {**field_names, "scheduleClass": "schedule_class"}
        orm_mode = True
        allow_population_by_field_name = True


class ObsScheduleClassResponse(Response):
    result: List[ObsScheduleClass]


class ObsScheduleClassWithStation(ObsScheduleClass):
    station: station_schema.Station


class ObsScheduleClassWithStationResponse(Response):
    result: List[ObsScheduleClassWithStation]




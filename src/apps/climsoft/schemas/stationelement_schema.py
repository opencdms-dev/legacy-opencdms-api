from typing import List
from pydantic import BaseModel, constr


field_names = {
    "recordedFrom": "recorded_from",
    "describedBy": "described_by",
    "recordedWith": "recorded_with",
    "instrumentcode": "instrument_code",
    "scheduledFor": "scheduled_for",
    "beginDate": "begin_date",
    "endDate": "end_date"
}


class CreateStationElement(BaseModel):
    recordedFrom: constr(max_length=255)
    describedBy: int
    recordedWith: constr(max_length=255)
    instrumentcode: constr(max_length=6)
    scheduledFor: constr(max_length=255)
    height: float
    beginDate: constr(max_length=50)
    endDate: constr(max_length=255)
    
    class Config:
        fields = field_names


class UpdateStationElement(CreateStationElement):
    pass


class StationElement(CreateStationElement):

    class Config:
        orm_mode = True
        fields = field_names
        allow_population_by_field_name = True


class StationElementResponse(BaseModel):
    message: str
    status: str
    result: List[StationElement]

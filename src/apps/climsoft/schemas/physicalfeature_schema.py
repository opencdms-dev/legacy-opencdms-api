import datetime

from pydantic import BaseModel, constr
from src.common_schemas import Response
from typing import List
from src.apps.climsoft.schemas import station_schema, physicalfeatureclass_schema


class CreatePhysicalFeature(BaseModel):
    associatedWith: constr(max_length=255)
    beginDate: constr(max_length=50)
    endDate: constr(max_length=50)
    image: constr(max_length=255)
    description: constr(max_length=255)
    classifiedInto: constr(max_length=50)

    class Config:
        fields = {
            "associatedWith": "associated_with",
            "beginDate": "begin_date",
            "endDate": "end_date",
            "classifiedInto": "classified_into",
        }


class UpdatePhysicalFeature(BaseModel):
    endDate: constr(max_length=50)
    image: constr(max_length=255)

    class Config:
        fields = {
            "endDate": "end_date"
        }


class PhysicalFeature(CreatePhysicalFeature):
    beginDate = datetime.datetime
    endDate = datetime.datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        fields = {
            "associatedWith": "associated_with",
            "beginDate": "begin_date",
            "endDate": "end_date",
            "classifiedInto": "classified_into",
        }
        

class PhysicalFeatureWithStationAndPhysicalFeatureClass(PhysicalFeature):
    station: station_schema.Station
    instrument: physicalfeatureclass_schema.PhysicalFeatureClass


class PhysicalFeatureResponse(Response):
    result: List[PhysicalFeature]


class PhysicalFeatureWithStationAndPhysicalFeatureClassResponse(Response):
    result: List[PhysicalFeatureWithStationAndPhysicalFeatureClass]




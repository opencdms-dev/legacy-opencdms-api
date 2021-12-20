from apps.climsoft.schemas import station_schema
from pydantic import BaseModel, constr
from common_schemas import Response
from typing import List


class CreatePhysicalFeatureClass(BaseModel):
    featureClass: constr(max_length=255)
    description: constr(max_length=255)
    refersTo: constr(max_length=255)

    class Config:
        fields = {
            "featureClass": "feature_class",
            "refersTo": "refers_to"
        }


class UpdatePhysicalFeatureClass(BaseModel):
    description: constr(max_length=255)
    refersTo: constr(max_length=255)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "refersTo": "refers_to"
        }


class PhysicalFeatureClass(BaseModel):
    featureClass: constr(max_length=255)
    description: constr(max_length=255)
    refersTo: constr(max_length=255)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "featureClass": "feature_class",
            "refersTo": "refers_to"
        }


class PhysicalFeatureClassWithStation(PhysicalFeatureClass):
    station: station_schema.Station


class PhysicalFeatureClassResponse(Response):
    result: List[PhysicalFeatureClass]


class PhysicalFeatureClassWithStationResponse(Response):
    result: List[PhysicalFeatureClassWithStation]

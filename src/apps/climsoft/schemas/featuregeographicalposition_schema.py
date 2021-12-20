from pydantic import BaseModel, constr
from common_schemas import Response
from typing import List
from apps.climsoft.schemas import synopfeature_schema


class CreateFeatureGeographicalPosition(BaseModel):
    belongsTo: constr(max_length=255)
    observedOn: constr(max_length=50)
    latitude: float
    longitude: float

    class Config:
        fields = {
            "belongsTo": "belongs_to",
            "observedOn": "observed_on"
        }


class UpdateFeatureGeographicalPosition(BaseModel):
    observedOn: constr(max_length=50)
    latitude: float
    longitude: float

    class Config:
        fields = {
            "observedOn": "observed_on"
        }


class FeatureGeographicalPosition(CreateFeatureGeographicalPosition):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "belongsTo": "belongs_to",
            "observedOn": "observed_on"
        }


class FeatureGeographicalPositionWithSynopFeature(FeatureGeographicalPosition):
    synopfeature: synopfeature_schema.SynopFeature


class FeatureGeographicalPositionResponse(Response):
    result: List[FeatureGeographicalPosition]


class FeatureGeographicalPositionWithSynopFeatureResponse(Response):
    result: List[FeatureGeographicalPositionWithSynopFeature]


from pydantic import BaseModel, constr
from src.common_schemas import Response
from typing import List
from src.apps.climsoft.schemas import synopfeature_schema


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
    synopfeature: synopfeature_schema.SynopFeature

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "belongsTo": "belongs_to",
            "observedOn": "observed_on"
        }


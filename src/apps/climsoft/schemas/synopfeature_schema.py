from pydantic import BaseModel, constr
from typing import List
from src.common_schemas import Response


class CreateSynopFeature(BaseModel):
    abbreviation: str
    description: constr(max_length=255)


class UpdateSynopFeature(BaseModel):
    description: constr(max_length=255)


class SynopFeature(CreateSynopFeature):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SynopFeatureResponse(Response):
    result: List[SynopFeature]









from pydantic import BaseModel, constr
from src.common_schemas import Response
from typing import List
from djantic import ModelSchema
from src.apps.surface import models


class CreateCountry(BaseModel):
    code: constr(max_length=2)
    name: constr(max_length=255)


class UpdateCountry(BaseModel):
    code: constr(max_length=2)


class Country(ModelSchema):
    code: constr(max_length=2)
    name: constr(max_length=255)

    class Config:
        model = models.Country


class CountryResponse(Response):
    result: List[Country]


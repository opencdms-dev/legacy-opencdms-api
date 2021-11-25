from typing import List
from src.common_schemas import Response
from pydantic import BaseModel, constr


class CreateFlag(BaseModel):
    characterSymbol: constr(max_length=255)
    numSymbol: int
    description: constr(max_length=255)

    class Config:
        fields = {
            "characterSymbol": "character_symbol",
            "numSymbol": "num_symbol"
        }


class UpdateFlag(BaseModel):
    numSymbol: int
    description: constr(max_length=255)

    class Config:
        fields = {
            "numSymbol": "num_symbol"
        }


class Flag(CreateFlag):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        fields = {
            "characterSymbol": "character_symbol",
            "numSymbol": "num_symbol"
        }


class FlagResponse(Response):
    result: List[Flag]

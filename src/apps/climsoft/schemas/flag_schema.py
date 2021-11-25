from typing import List
from src.common_schemas import Response
from pydantic import BaseModel, constr


class CreateFlag(BaseModel):
    characterSymbol: constr(max_length=255)
    numSymbol: int
    description: constr(max_length=255)


class UpdateFlag(BaseModel):
    numSymbol: int
    description: constr(max_length=255)


class Flag(CreateFlag):
    class Config:
        orm_mode = True


class FlagResponse(Response):
    result: List[Flag]

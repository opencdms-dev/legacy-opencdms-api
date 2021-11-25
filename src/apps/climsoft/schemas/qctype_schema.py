from pydantic import BaseModel, constr
from typing import List
from src.common_schemas import Response


class CreateQCType(BaseModel):
    code: int
    description: constr(max_length=255)


class UpdateQCType(BaseModel):
    description: constr(max_length=255)


class QCType(CreateQCType):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class QCTypeResponse(Response):
    result: List[QCType]









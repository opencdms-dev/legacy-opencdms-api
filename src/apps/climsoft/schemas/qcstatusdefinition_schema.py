from pydantic import BaseModel, constr
from typing import List
from common_schemas import Response


class CreateQCStatusDefinition(BaseModel):
    code: int
    description: constr(max_length=255)


class UpdateQCStatusDefinition(BaseModel):
    description: constr(max_length=255)


class QCStatusDefinition(CreateQCStatusDefinition):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class QCStatusDefinitionResponse(Response):
    result: List[QCStatusDefinition]









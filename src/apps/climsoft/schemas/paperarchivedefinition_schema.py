from pydantic import BaseModel, constr
from typing import List
from src.common_schemas import Response


class CreatePaperArchiveDefinition(BaseModel):
    formId: constr(max_length=50)
    description: constr(max_length=255)

    class Config:
        fields = {"formId": "form_id"}


class UpdatePaperArchiveDefinition(BaseModel):
    description: constr(max_length=255)


class PaperArchiveDefinition(CreatePaperArchiveDefinition):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {"formId": "form_id"}


class PaperArchiveDefinitionResponse(Response):
    result: List[PaperArchiveDefinition]









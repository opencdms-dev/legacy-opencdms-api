import datetime

from pydantic import BaseModel, constr
from common_schemas import Response
from apps.climsoft.schemas import station_schema, paperarchivedefinition_schema
from typing import List


class CreatePaperArchive(BaseModel):
    belongsTo: constr(max_length=255)
    formDatetime: str
    image: constr(max_length=255)
    classifiedInto: constr(max_length=50)

    class Config:
        fields = {
            "belongsTo": "belongs_to",
            "formDatetime": "form_datetime",
            "classifiedInto": "classified_into"
        }


class UpdatePaperArchive(BaseModel):
    image: constr(max_length=255)


class PaperArchive(CreatePaperArchive):
    formDatetime: datetime.datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "belongsTo": "belongs_to",
            "formDatetime": "form_datetime",
            "classifiedInto": "classified_into"
        }


class PaperArchiveResponse(Response):
    result: List[PaperArchive]


class PaperArchiveWithStationAndPaperArchiveDefinition(PaperArchive):
    station: station_schema.Station
    paperarchivedefinition: paperarchivedefinition_schema.PaperArchiveDefinition


class PaperArchiveWithStationAndPaperArchiveDefinitionResponse(Response):
    result: List[PaperArchiveWithStationAndPaperArchiveDefinition]




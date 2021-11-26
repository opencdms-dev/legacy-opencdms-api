import datetime

from pydantic import BaseModel, constr
from src.common_schemas import Response
from src.apps.climsoft.schemas import station_schema, paperarchivedefinition_schema
from typing import List


class CreatePaperArchive(BaseModel):
    belongsTo: constr(max_length=255)
    fromDatetime: datetime.datetime
    image: constr(max_length=255)
    classifiedInfo: constr(max_length=50)

    class Config:
        fields = {
            "belongsTo": "belongs_to",
            "fromDatetime": "from_datetime",
            "classifiedInfo": "classified_info"
        }


class UpdatePaperArchive(BaseModel):
    fromDatetime: datetime.datetime
    image: constr(max_length=255)
    classifiedInfo: constr(max_length=50)

    class Config:
        fields = {
            "fromDatetime": "from_datetime",
            "classifiedInfo": "classified_info"
        }


class PaperArchive(CreatePaperArchive):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "belongsTo": "belongs_to",
            "fromDatetime": "from_datetime",
            "classifiedInfo": "classified_info"
        }


class PaperArchiveResponse(Response):
    result: List[PaperArchive]


class PaperArchiveWithStationAndPaperArchiveDefinition(PaperArchive):
    station: station_schema.Station
    paperarchivedefinition: paperarchivedefinition_schema.PaperArchiveDefinition


class PaperArchiveWithStationAndPaperArchiveDefinitionResponse(Response):
    result: List[PaperArchiveWithStationAndPaperArchiveDefinition]




import datetime

from pydantic import BaseModel, constr
from common_schemas import Response
from typing import List
from apps.climsoft.schemas import instrumentfaultreport_schema


class CreateFaultResolution(BaseModel):
    resolvedDatetime: constr(max_length=50)
    associatedWith: constr(max_length=255)
    resolvedBy: constr(max_length=255)
    remarks: constr(max_length=255)

    class Config:
        fields = {
            "resolvedDatetime": "resolved_datetime",
            "resolvedBy": "resolved_by",
            "associatedWith": "associated_with"
        }


class UpdateFaultResolution(BaseModel):
    resolvedBy: constr(max_length=255)
    remarks: constr(max_length=255)

    class Config:
        fields = {
            "resolvedBy": "resolved_by"
        }


class FaultResolution(CreateFaultResolution):
    resolvedDatetime = datetime.datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

        fields = {
            "resolvedDatetime": "resolved_datetime",
            "resolvedBy": "resolved_by",
            "associatedWith": "associated_with"
        }


class FaultResolutionWithInstrumentFaultReport(FaultResolution):
    instrumentfaultreport: instrumentfaultreport_schema.InstrumentFaultReport


class FaultResolutionResponse(Response):
    result: List[FaultResolution]


class FaultResolutionWithInstrumentFaultReportResponse(Response):
    result: List[FaultResolutionWithInstrumentFaultReport]




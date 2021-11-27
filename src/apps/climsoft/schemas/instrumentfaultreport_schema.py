from pydantic import BaseModel, constr
from src.common_schemas import Response
from typing import List
from src.apps.climsoft.schemas import station_schema, instrument_schema


class CreateInstrumentFaultReport(BaseModel):
    refersTo: constr(max_length=255)
    reportId: constr(max_length=255)
    reportDatetime: constr(max_length=50)
    faultDescription: constr(max_length=255)
    reportedBy: constr(max_length=255)
    receivedDatetime: constr(max_length=50)
    receivedBy: constr(max_length=255)
    reportedFrom: constr(max_length=255)

    class Config:
        fields = {
            "refersTo": "refers_to",
            "reportId": "report_id",
            "reportDatetime": "report_datetime",
            "reportDescription": "report_description",
            "reportedBy": "reported_by",
            "receivedDatetime": "received_datetime",
            "receivedBy": "received_by",
            "reportedFrom": "reported_from"
        }


class UpdateInstrumentFaultReport(BaseModel):
    refersTo: constr(max_length=255)
    reportDatetime: constr(max_length=50)
    faultDescription: constr(max_length=255)
    reportedBy: constr(max_length=255)
    receivedDatetime: constr(max_length=50)
    receivedBy: constr(max_length=255)
    reportedFrom: constr(max_length=255)

    class Config:
        fields = {
            "refersTo": "refers_to",
            "reportDatetime": "report_datetime",
            "reportDescription": "report_description",
            "reportedBy": "reported_by",
            "receivedDatetime": "received_datetime",
            "receivedBy": "received_by",
            "reportedFrom": "reported_from"
        }


class InstrumentFaultReport(CreateInstrumentFaultReport):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "refersTo": "refers_to",
            "reportId": "report_id",
            "reportDatetime": "report_datetime",
            "reportDescription": "report_description",
            "reportedBy": "reported_by",
            "receivedDatetime": "received_datetime",
            "receivedBy": "received_by",
            "reportedFrom": "reported_from"
        }


class InstrumentFaultReportWithStationAndInstrument(InstrumentFaultReport):
    station: station_schema.Station
    instrument: instrument_schema.Instrument


class InstrumentFaultReportResponse(Response):
    result: List[InstrumentFaultReport]


class InstrumentFaultReportWithStationAndInstrumentResponse(Response):
    result: List[InstrumentFaultReportWithStationAndInstrument]




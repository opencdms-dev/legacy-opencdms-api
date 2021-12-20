import datetime
from typing import List
from pydantic import BaseModel, constr
from apps.climsoft.schemas import Response, obselement_schema, station_schema


field_names_no_pk = {
    "obsLevel": "obs_level",
    "obsValue": "obs_value",
    "qcTypeLog": "qc_type_log",
    "dataForm": "data_form",
    "capturedBy": "captured_by",
    "temperatureUnits": "temperature_units",
    "precipitationUnits": "precipitation_units",
    "cloudHeightUnits": "cloud_height_units",
    "visUnits": "vis_units",
    "dataSourceTimeZone": "data_source_timezone"
}


field_names_all = {
    **field_names_no_pk,
    "recordedFrom": "recorded_from",
    "describedBy": "described_by",
    "obsDatetime": "obs_datetime",
    "qcStatus": "qc_status",
    "acquisitionType": "acquisition_type"
}


class CreateObservationInitial(BaseModel):
    recordedFrom: constr(max_length=255)
    describedBy: int
    obsDatetime: str
    qcStatus: int
    acquisitionType: int
    obsLevel: constr(max_length=255)
    obsValue: constr(max_length=255)
    flag: constr(max_length=255)
    period: int
    qcTypeLog: str
    dataForm: constr(max_length=255)
    capturedBy: constr(max_length=255)
    mark: bool
    temperatureUnits: constr(max_length=255)
    precipitationUnits: constr(max_length=255)
    cloudHeightUnits: constr(max_length=255)
    visUnits: constr(max_length=255)
    dataSourceTimeZone: int

    class Config:
        fields = field_names_all


class UpdateObservationInitial(BaseModel):
    obsLevel: constr(max_length=255)
    obsValue: constr(max_length=255)
    flag: constr(max_length=255)
    period: int
    qcTypeLog: str
    dataForm: constr(max_length=255)
    capturedBy: constr(max_length=255)
    mark: bool
    temperatureUnits: constr(max_length=255)
    precipitationUnits: constr(max_length=255)
    cloudHeightUnits: constr(max_length=255)
    visUnits: constr(max_length=255)
    dataSourceTimeZone: int

    class Config:
        fields = field_names_no_pk


class ObservationInitial(CreateObservationInitial):
    obsDatetime: datetime.datetime

    class Config:
        orm_mode = True
        fields = field_names_all
        allow_population_by_field_name = True


class ObservationInitialResponse(Response):
    result: List[ObservationInitial]


class ObservationInitialWithChildren(ObservationInitial):
    obselement: obselement_schema.ObsElement
    station: station_schema.Station

    class Config:
        orm_mode = True
        fields = {**field_names_all, "obselement": "obs_element"}
        allow_population_by_field_name = True


class ObservationInitialWithChildrenResponse(Response):
    result: List[ObservationInitialWithChildren]


class ObservationInitialInputGen(CreateObservationInitial):
    class Config:
        fields = field_names_all
        allow_population_by_field_name = True

import datetime
from typing import List, Optional
from pydantic import BaseModel, constr
from src.apps.climsoft.schemas import Response, obselement_schema, station_schema


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
    "dataSourceTimeZone": "data_source_timezone",
    "qcStatus": "qc_status",
    "acquisitionType": "acquisition_type"
}


field_names_all = {
    **field_names_no_pk,
    "recordedFrom": "recorded_from",
    "describedBy": "described_by",
    "obsDatetime": "obs_datetime"
}


class CreateObservationFinal(BaseModel):
    recordedFrom: constr(max_length=255)
    describedBy: int
    obsDatetime: str
    qcStatus: int
    acquisitionType: int
    obsLevel: constr(max_length=255)
    obsValue: constr(max_length=255)
    flag: constr(max_length=255)
    period: Optional[int]
    qcTypeLog: Optional[str]
    dataForm: Optional[constr(max_length=255)]
    capturedBy: Optional[constr(max_length=255)]
    mark: Optional[bool]
    temperatureUnits: Optional[constr(max_length=255)]
    precipitationUnits: Optional[constr(max_length=255)]
    cloudHeightUnits: Optional[constr(max_length=255)]
    visUnits: Optional[constr(max_length=255)]
    dataSourceTimeZone: int

    class Config:
        fields = field_names_all


class UpdateObservationFinal(BaseModel):
    qcStatus: int
    acquisitionType: int
    obsLevel: constr(max_length=255)
    obsValue: constr(max_length=255)
    flag: constr(max_length=255)
    period: Optional[int]
    qcTypeLog: Optional[str]
    dataForm: Optional[constr(max_length=255)]
    capturedBy: Optional[constr(max_length=255)]
    mark: Optional[bool]
    temperatureUnits: Optional[constr(max_length=255)]
    precipitationUnits: Optional[constr(max_length=255)]
    cloudHeightUnits: Optional[constr(max_length=255)]
    visUnits: Optional[constr(max_length=255)]
    dataSourceTimeZone: int

    class Config:
        fields = field_names_no_pk


class ObservationFinal(CreateObservationFinal):
    obsDatetime: datetime.datetime

    class Config:
        orm_mode = True
        fields = field_names_all
        allow_population_by_field_name = True


class ObservationFinalResponse(Response):
    result: List[ObservationFinal]


class ObservationFinalWithChildren(ObservationFinal):
    obselement: obselement_schema.ObsElement
    station: station_schema.Station

    class Config:
        orm_mode = True
        fields = {**field_names_all, "obselement": "obs_element"}
        allow_population_by_field_name = True


class ObservationFinalWithChildrenResponse(Response):
    result: List[ObservationFinalWithChildren]


class ObservationFinalInputGen(CreateObservationFinal):
    class Config:
        fields = field_names_all
        allow_population_by_field_name = True



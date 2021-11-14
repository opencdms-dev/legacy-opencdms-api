import datetime
from typing import List
from pydantic import BaseModel, constr


class CreateStation(BaseModel):
    stationId: constr(max_length=255)
    stationName: constr(max_length=255)
    wmoid: constr(max_length=20)
    icaoid: constr(max_length=20)
    latitude: float
    qualifier: constr(max_length=20)
    longitude: float
    elevation: constr(max_length=255)
    geoLocationMethod: constr(max_length=255)
    geoLocationAccuracy: float
    openingDatetime: datetime.datetime
    closingDatetime: datetime.datetime
    country: constr(max_length=50)
    authority: constr(max_length=255)
    adminRegion: constr(max_length=255)
    drainageBasin: constr(max_length=255)
    wacaSelection: bool
    cptSelection: bool
    stationOperational: bool

    class Config:
        fields = {
            "stationId": "station_id",
            "stationName": "station_name",
            "geoLocationMethod": "geolocation_method",
            "geoLocationAccuracy": "geolocation_accuracy",
            "openingDatetime": "opening_datetime",
            "closingDatetime": "closing_datetime",
            "adminRegion": "admin_region",
            "drainageBasin": "drainage_basin",
            "wacaSelection": "waca_selection",
            "cptSelection": "cpt_selection",
            "stationOperational": "station_operational"
        }


class UpdateStation(BaseModel):
    stationName: constr(max_length=255)
    wmoid: constr(max_length=20)
    icaoid: constr(max_length=20)
    latitude: float
    qualifier: constr(max_length=20)
    longitude: float
    elevation: constr(max_length=255)
    geoLocationMethod: constr(max_length=255)
    geoLocationAccuracy: float
    openingDatetime: datetime.datetime
    closingDatetime: datetime.datetime
    country: constr(max_length=50)
    authority: constr(max_length=255)
    adminRegion: constr(max_length=255)
    drainageBasin: constr(max_length=255)
    wacaSelection: bool
    cptSelection: bool
    stationOperational: bool

    class Config:
        fields = {
            "stationName": "station_name",
            "geoLocationMethod": "geolocation_method",
            "geoLocationAccuracy": "geolocation_accuracy",
            "openingDatetime": "opening_datetime",
            "closingDatetime": "closing_datetime",
            "adminRegion": "admin_region",
            "drainageBasin": "drainage_basin",
            "wacaSelection": "waca_selection",
            "cptSelection": "cpt_selection",
            "stationOperational": "station_operational"
        }


class Station(CreateStation):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class StationResponse(BaseModel):
    result: List[Station]
    message: str
    status: str


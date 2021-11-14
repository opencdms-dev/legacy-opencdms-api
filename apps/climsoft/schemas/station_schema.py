import datetime
from typing import List
from pydantic import BaseModel, constr


class CreateStation(BaseModel):
    station_id: constr(max_length=255)
    station_name: constr(max_length=255)
    wmoid: constr(max_length=20)
    icaoid: constr(max_length=20)
    latitude: float
    qualifier: constr(max_length=20)
    longitude: float
    elevation: constr(max_length=255)
    geolocation_method: constr(max_length=255)
    geolocation_accuracy: float
    opening_datetime: datetime.datetime
    closing_datetime: datetime.datetime
    country: constr(max_length=50)
    authority: constr(max_length=255)
    admin_region: constr(max_length=255)
    drainage_basin: constr(max_length=255)
    waca_selection: bool
    cpt_selection: bool
    station_operational: bool

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
    station_name: constr(max_length=255)
    wmoid: constr(max_length=20)
    icaoid: constr(max_length=20)
    latitude: float
    qualifier: constr(max_length=20)
    longitude: float
    elevation: constr(max_length=255)
    geolocation_method: constr(max_length=255)
    geolocation_accuracy: float
    opening_datetime: datetime.datetime
    closing_datetime: datetime.datetime
    country: constr(max_length=50)
    authority: constr(max_length=255)
    admin_region: constr(max_length=255)
    drainage_basin: constr(max_length=255)
    waca_selection: bool
    cpt_selection: bool
    station_operational: bool

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


class StationResponse(BaseModel):
    result: List[Station]
    message: str
    status: str


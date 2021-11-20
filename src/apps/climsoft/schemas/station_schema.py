import datetime
from typing import List, Optional
from pydantic import BaseModel, constr


class CreateStation(BaseModel):
    stationId: constr(max_length=255)
    stationName: constr(max_length=255)
    wmoid: Optional[constr(max_length=20)]
    icaoid: Optional[constr(max_length=20)]
    latitude: float
    qualifier: Optional[constr(max_length=20)]
    longitude: float
    elevation: constr(max_length=255)
    geoLocationMethod: Optional[constr(max_length=255)]
    geoLocationAccuracy: Optional[float]
    openingDatetime: Optional[datetime.datetime]
    closingDatetime: datetime.datetime
    country: constr(max_length=50)
    authority: Optional[constr(max_length=255)]
    adminRegion: Optional[constr(max_length=255)]
    drainageBasin: Optional[constr(max_length=255)]
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
    wmoid: Optional[constr(max_length=20)]
    icaoid: Optional[constr(max_length=20)]
    latitude: float
    qualifier: Optional[constr(max_length=20)]
    longitude: float
    elevation: constr(max_length=255)
    geoLocationMethod: Optional[constr(max_length=255)]
    geoLocationAccuracy: Optional[float]
    openingDatetime: Optional[datetime.datetime]
    closingDatetime: datetime.datetime
    country: constr(max_length=50)
    authority: Optional[constr(max_length=255)]
    adminRegion: Optional[constr(max_length=255)]
    drainageBasin: Optional[constr(max_length=255)]
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
    openingDatetime: Optional[str]
    closingDatetime: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class StationResponse(BaseModel):
    result: List[Station]
    message: str
    status: str


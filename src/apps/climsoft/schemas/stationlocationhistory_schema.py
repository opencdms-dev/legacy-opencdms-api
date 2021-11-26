from src.apps.climsoft.schemas import station_schema
from pydantic import BaseModel, constr
from src.common_schemas import Response
from typing import List


class CreateStationLocationHistory(BaseModel):
    belongsTo: constr(max_length=255)
    openingDatetime: str
    stationType: constr(max_length=255)
    geoLocationMethod: constr(max_length=255)
    geoLocationAccuracy: float
    closingDatetime: str
    latitude: float
    longitude: float
    elevation: int
    authority: constr(max_length=255)
    adminRegion: constr(max_length=255)
    drainageBasin: constr(max_length=255)

    class Config:
        fields = {
            "belongsTo": "belongs_to",
            "stationType": "station_type",
            "geolocation_method": "geolocationMethod",
            "openingDatetime": "opening_datetime",
            "closingDatetime": "closing_datetime",
            "adminRegion": "admin_region",
            "drainageBasin": "drainage_basin"
        }


class UpdateStationLocationHistory(BaseModel):
    stationType: constr(max_length=255)
    geoLocationMethod: constr(max_length=255)
    geoLocationAccuracy: float
    closingDatetime: str
    latitude: float
    longitude: float
    elevation: int
    authority: constr(max_length=255)
    adminRegion: constr(max_length=255)
    drainageBasin: constr(max_length=255)

    class Config:
        fields = {
            "stationType": "station_type",
            "geolocation_method": "geolocationMethod",
            "closingDatetime": "closing_datetime",
            "adminRegion": "admin_region",
            "drainageBasin": "drainage_basin"
        }


class StationLocationHistory(BaseModel):
    stationType: constr(max_length=255)
    geoLocationMethod: constr(max_length=255)
    geoLocationAccuracy: float
    closingDatetime: str
    latitude: float
    longitude: float
    elevation: int
    authority: constr(max_length=255)
    adminRegion: constr(max_length=255)
    drainageBasin: constr(max_length=255)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "belongsTo": "belongs_to",
            "stationType": "station_type",
            "geolocation_method": "geolocationMethod",
            "openingDatetime": "opening_datetime",
            "closingDatetime": "closing_datetime",
            "adminRegion": "admin_region",
            "drainageBasin": "drainage_basin"
        }


class StationLocationHistoryWithStation(StationLocationHistory):
    station: station_schema.Station


class StationLocationHistoryResponse(Response):
    result: List[StationLocationHistory]


class StationLocationHistoryWithStationResponse(Response):
    result: List[StationLocationHistoryWithStation]

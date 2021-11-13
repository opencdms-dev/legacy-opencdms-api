import datetime
from pydantic import BaseModel, constr


class CreateStation(BaseModel):
    stationId: constr(max_length=255)
    stationName: constr(max_length=255)
    wmoid: constr(max_length=20)
    icaoid: constr(max_length=20)
    lattitude: float
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


class UpdateStation(BaseModel):
    stationName: constr(max_length=255)
    wmoid: constr(max_length=20)
    icaoid: constr(max_length=20)
    lattitude: float
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


class Station(CreateStation):
    class Config:
        orm_mode = True


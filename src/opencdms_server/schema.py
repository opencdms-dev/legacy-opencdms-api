from pydantic import BaseModel


class StationSchema(BaseModel):
    """Station response schema"""

    stationId: str
    stationName: str
    wmoid: str
    icaoid: str
    latitude: float
    qualifier: str
    longitude: float
    elevation: str
    geoLocationMethod: str
    geoLocationAccuracy: float
    openingDatetime: str
    closingDatetime: str
    country: str
    authority: str
    adminRegion: str
    drainageBasin: str
    wacaSelection: int
    cptSelection: int
    stationOperational: int

    class Config:
        orm_mode = True

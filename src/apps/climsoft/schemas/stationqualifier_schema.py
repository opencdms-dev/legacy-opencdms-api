from pydantic import BaseModel, constr
from src.common_schemas import Response
from typing import List
from src.apps.climsoft.schemas import station_schema


class CreateStationQualifier(BaseModel):
    qualifier: constr(max_length=255)
    qualifierBeginDate: constr(max_length=50)
    qualifierEndDate: constr(max_length=50)
    belongsTo: constr(max_length=255)
    stationTimeZone: int
    stationNetworkType: constr(max_length=255)

    class Config:
        fields = {
            "qualifierBeginDate": "qualifier_begin_date",
            "qualifierEndDate": "qualifier_end_date",
            "belongsTo": "belongs_to",
            "stationTimeZone": "station_timezone",
            "stationNetworkType": "station_network_type"
        }


class UpdateStationQualifier(BaseModel):
    stationTimeZone: int
    stationNetworkType: constr(max_length=255)

    class Config:
        fields = {
            "stationTimeZone": "station_timezone",
            "stationNetworkType": "station_network_type"
        }


class StationQualifier(CreateStationQualifier):

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "qualifierBeginDate": "qualifier_begin_date",
            "qualifierEndDate": "qualifier_end_date",
            "belongsTo": "belongs_to",
            "stationTimeZone": "station_timezone",
            "stationNetworkType": "station_network_type"
        }


class StationQualifierResponse(Response):
    result: List[StationQualifier]


class StationQualifierWithStation(StationQualifier):
    station: station_schema.Station


class StationQualifierWithStationResponse(Response):
    result: List[StationQualifierWithStation]

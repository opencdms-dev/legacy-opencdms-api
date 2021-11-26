import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import stationlocationhistory_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftStationLocationHistoryService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingStationLocationHistory(Exception):
    pass


class FailedGettingStationLocationHistory(Exception):
    pass


class FailedGettingStationLocationHistoryList(Exception):
    pass


class FailedUpdatingStationLocationHistory(Exception):
    pass


class FailedDeletingStationLocationHistory(Exception):
    pass


class StationLocationHistoryDoesNotExist(Exception):
    pass


def create(db_session: Session, data: stationlocationhistory_schema.CreateStationLocationHistory) -> stationlocationhistory_schema.StationLocationHistory:
    try:
        station_location_history = models.Stationlocationhistory(**data.dict())
        db_session.add(station_location_history)
        db_session.commit()
        return stationlocationhistory_schema.StationLocationHistory.from_orm(station_location_history)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingStationLocationHistory("Failed creating station_location_history.")


def get(db_session: Session, belongs_to: str, opening_datetime: str) -> stationlocationhistory_schema.StationLocationHistory:
    try:
        station_location_history = db_session.query(models.Stationlocationhistory).filter_by(featureClass=feature_class).options(joinedload('station')).first()

        if not station_location_history:
            raise HTTPException(status_code=404, detail="StationLocationHistory does not exist.")

        return stationlocationhistory_schema.StationLocationHistoryWithStation.from_orm(station_location_history)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingStationLocationHistory("Failed getting station_location_history.")


def query(
    db_session: Session,
    belongs_to: str = None,
    station_type: str = None,
    geolocation_method: str = None,
    geolocation_accuracy: float = None,
    opening_datetime: str = None,
    closing_datetime: str = None,
    latitude: float = None,
    longitude: float = None,
    elevation: int = None,
    authority: str = None,
    admin_region: str = None,
    drainage_basin: str = None,
    limit: int = 25,
    offset: int = 0
) -> List[stationlocationhistory_schema.StationLocationHistory]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `station_location_history` row skipping
    `offset` number of rows
    """
    try:
        q = db_session.query(models.Stationlocationhistory)

        if belongs_to is not None:
            q = q.filter_by(belongsTo=belongs_to)

        if station_type is not None:
            q = q.filter_by(stationType=station_type)

        if geolocation_method is not None:
            q = q.filter_by(geoLocationMethod=geolocation_method)

        if geolocation_accuracy is not None:
            q = q.filter_by(geoLocationAccuracy=geolocation_accuracy)

        if opening_datetime is not None:
            q = q.filter_by(openingDatetime=opening_datetime)

        if closing_datetime is not None:
            q = q.filter_by(closingDatetime=closing_datetime)

        if latitude is not None:
            q = q.filter_by(latitude=latitude)

        if longitude is not None:
            q = q.filter_by(longitude=longitude)

        if elevation is not None:
            q = q.filter_by(elevation=elevation)

        if authority is not None:
            q = q.filter_by(authority=authority)

        if admin_region is not None:
            q = q.filter_by(adminRegion=admin_region)

        if drainage_basin is not None:
            q = q.filter_by(drainageBasin=drainage_basin)

        return [stationlocationhistory_schema.StationLocationHistory.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingStationLocationHistoryList("Failed getting station_location_history list.")


def update(db_session: Session, belongs_to: str, opening_datetime: str, updates: stationlocationhistory_schema.UpdateStationLocationHistory) -> stationlocationhistory_schema.StationLocationHistory:
    try:
        db_session.query(models.Stationlocationhistory).filter_by(belongsTo=belongs_to, openingDatetime=opening_datetime).update(updates.dict())
        db_session.commit()
        updated_station_location_history = db_session.query(models.Stationlocationhistory).filter_by(belongsTo=belongs_to, openingDatetime=opening_datetime).first()
        return stationlocationhistory_schema.StationLocationHistory.from_orm(updated_station_location_history)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingStationLocationHistory("Failed updating station_location_history")


def delete(db_session: Session, belongs_to: str, opening_datetime: str) -> bool:
    try:
        db_session.query(models.Stationlocationhistory).filter_by(belongsTo=belongs_to, openingDatetime=opening_datetime).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingStationLocationHistory("Failed deleting station_location_history.")





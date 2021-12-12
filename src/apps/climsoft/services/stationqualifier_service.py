import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from apps.climsoft.schemas import stationqualifier_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftStationQualifierService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingStationQualifier(Exception):
    pass


class FailedGettingStationQualifier(Exception):
    pass


class FailedGettingStationQualifierList(Exception):
    pass


class FailedUpdatingStationQualifier(Exception):
    pass


class FailedDeletingStationQualifier(Exception):
    pass


class StationQualifierDoesNotExist(Exception):
    pass


def create(db_session: Session, data: stationqualifier_schema.CreateStationQualifier) -> stationqualifier_schema.StationQualifier:
    try:
        station_qualifier = models.Stationqualifier(**data.dict())
        db_session.add(station_qualifier)
        db_session.commit()
        return stationqualifier_schema.StationQualifier.from_orm(station_qualifier)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingStationQualifier("Failed creating station_qualifier.")


def get(db_session: Session, qualifier: str, qualifier_begin_date: str, qualifier_end_date: str, belongs_to: str) -> stationqualifier_schema.StationQualifier:
    try:
        station_qualifier = db_session.query(models.Stationqualifier).filter_by(
            qualifier=qualifier,
            qualifierBeginDate=qualifier_begin_date,
            qualifierEndDate=qualifier_end_date,
            belongsTo=belongs_to
        ).options(joinedload('station')).first()

        if not station_qualifier:
            raise HTTPException(status_code=404, detail="StationQualifier does not exist.")

        print(stationqualifier_schema.StationQualifierWithStation.schema(by_alias=True))

        return stationqualifier_schema.StationQualifierWithStation.from_orm(station_qualifier)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingStationQualifier("Failed getting station_qualifier.")


def query(
    db_session: Session,
    qualifier: str = None,
    qualifier_begin_date: str = None,
    qualifier_end_date: str = None,
    station_timezone: int = None,
    station_network_type: str = None,
    belongs_to: str = None,
    limit: int = 25,
    offset: int = 0
) -> List[stationqualifier_schema.StationQualifier]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `station_qualifier` row skipping
    `offset` number of rows
    """
    try:
        q = db_session.query(models.Stationqualifier)

        if qualifier is not None:
            q = q.filter_by(qualifier=qualifier)

        if qualifier_begin_date is not None:
            q = q.filter_by(qualifierBeginDate=qualifier_begin_date)

        if qualifier_end_date is not None:
            q = q.filter_by(qualifierEndDate=qualifier_end_date)

        if station_timezone is not None:
            q = q.filter_by(stationTimeZone=station_timezone)

        if station_network_type is not None:
            q = q.filter_by(stationNetworkType=station_network_type)

        if belongs_to is not None:
            q = q.filter_by(belongsTo=belongs_to)

        return [stationqualifier_schema.StationQualifier.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingStationQualifierList("Failed getting station_qualifier list.")


def update(db_session: Session, qualifier: str, qualifier_begin_date: str, qualifier_end_date: str, belongs_to: str, updates: stationqualifier_schema.UpdateStationQualifier) -> stationqualifier_schema.StationQualifier:
    try:
        db_session.query(models.Stationqualifier).filter_by(
            qualifier=qualifier,
            qualifierBeginDate=qualifier_begin_date,
            qualifierEndDate=qualifier_end_date,
            belongsTo=belongs_to
        ).update(updates.dict())
        db_session.commit()
        updated_station_qualifier = db_session.query(models.Stationqualifier).filter_by(
            qualifier=qualifier,
            qualifierBeginDate=qualifier_begin_date,
            qualifierEndDate=qualifier_end_date,
            belongsTo=belongs_to
        ).first()
        return stationqualifier_schema.StationQualifier.from_orm(updated_station_qualifier)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingStationQualifier("Failed updating station_qualifier")


def delete(db_session: Session, qualifier: str, qualifier_begin_date: str, qualifier_end_date: str, belongs_to: str) -> bool:
    try:
        db_session.query(models.Stationqualifier).filter_by(
            qualifier=qualifier,
            qualifierBeginDate=qualifier_begin_date,
            qualifierEndDate=qualifier_end_date,
            belongsTo=belongs_to
        ).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingStationQualifier("Failed deleting station_qualifier.")





import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import stationelement_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftStationElementService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingStationElement(Exception):
    pass


class FailedGettingStationElement(Exception):
    pass


class FailedGettingStationElementList(Exception):
    pass


class FailedUpdatingStationElement(Exception):
    pass


class FailedDeletingStationElement(Exception):
    pass


class StationElementDoesNotExist(Exception):
    pass


def create(db_session: Session, data: stationelement_schema.CreateStationElement) -> stationelement_schema.StationElement:
    try:
        station_element = models.Stationelement(**data.dict())
        db_session.add(station_element)
        db_session.commit()
        return stationelement_schema.StationElement.from_orm(station_element)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingStationElement("Failed creating station_element.")


def get(db_session: Session, recorded_from: str, described_by: int, recorded_with: str, begin_date: str) -> stationelement_schema.StationElementWithChildren:
    try:
        station_element = db_session.query(models.Stationelement)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(recordedWith=recorded_with)\
            .filter_by(beginDate=begin_date)\
            .options(joinedload("obselement"), joinedload("station"), joinedload("station_element"), joinedload("obsscheduleclas"))\
            .first()

        if not station_element:
            raise HTTPException(status_code=404, detail="StationElement does not exist.")

        return stationelement_schema.StationElementWithChildren.from_orm(station_element)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingStationElement("Failed getting station_element.")


def query(
        db_session: Session,
        recorded_from: str = None,
        described_by: int = None,
        recorded_with: str = None,
        instrument_code: str = None,
        scheduled_for: str = None,
        height: int = None,
        begin_date: float = None,
        end_date: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[stationelement_schema.StationElement]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `stationelement` row skipping
    `offset` number of rows
    :param db_session: database session
    :param recorded_from: filter by station
    :param described_by: filter by obselement
    :param recorded_with: filter by instrument
    :param instrument_code: compares `instrumentcode` column for exact match
    :param scheduled_for: filter by obsscheduleclass
    :param height: returns items with greater or equal height
    :param begin_date: returns items with greater or equal begin_date
    :param end_date: returns items with smaller or equal end_date
    :param limit: returns first `limit` number of records
    :param offset: skips first `offset` number of records
    :return: list of `stationelement`
    """
    try:
        q = db_session.query(models.Stationelement)

        if recorded_from is not None:
            q = q.filter_by(recordedFrom=recorded_from)

        if described_by is not None:
            q = q.filter_by(describedBy=described_by)

        if recorded_with is not None:
            q = q.filter_by(recordedWith=recorded_with)

        if instrument_code is not None:
            q = q.filter_by(instrumentcode=instrument_code)

        if scheduled_for is not None:
            q = q.filter_by(scheduledFor=scheduled_for)

        if height is not None:
            q = q.filter(models.Stationelement.height >= height)

        if begin_date is not None:
            q = q.filter(models.Stationelement.beginDate >= begin_date)

        if end_date is not None:
            q = q.filter(models.Stationelement.endDate <= end_date)

        return [stationelement_schema.StationElement.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingStationElementList("Failed getting station_element list.")


def update(db_session: Session, recorded_from: str, described_by: int, recorded_with: str, begin_date: str, updates: stationelement_schema.UpdateStationElement) -> stationelement_schema.StationElement:
    try:
        db_session.query(models.Stationelement).filter_by(recordedFrom=recorded_from).filter_by(describedBy=described_by).filter_by(recordedWith=recorded_with).filter_by(beginDate=begin_date).update(updates.dict())
        db_session.commit()
        updated_instrument = db_session.query(models.Stationelement).filter_by(recordedFrom=recorded_from).filter_by(describedBy=described_by).filter_by(recordedWith=recorded_with).filter_by(beginDate=begin_date).first()
        return stationelement_schema.StationElement.from_orm(updated_instrument)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingStationElement("Failed updating station_element")


def delete(db_session: Session, recorded_from: str, described_by: int, recorded_with: str, begin_date: str) -> bool:
    try:
        db_session.query(models.Stationelement).filter_by(recordedFrom=recorded_from).filter_by(describedBy=described_by).filter_by(recordedWith=recorded_with).filter_by(beginDate=begin_date).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingStationElement("Failed deleting station_element.")





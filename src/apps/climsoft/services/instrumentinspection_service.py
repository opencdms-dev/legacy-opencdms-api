import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import instrumentinspection_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftInstrumentInspectionService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingInstrumentInspection(Exception):
    pass


class FailedGettingInstrumentInspection(Exception):
    pass


class FailedGettingInstrumentInspectionList(Exception):
    pass


class FailedUpdatingInstrumentInspection(Exception):
    pass


class FailedDeletingInstrumentInspection(Exception):
    pass


class InstrumentInspectionDoesNotExist(Exception):
    pass


def create(db_session: Session, data: instrumentinspection_schema.CreateInstrumentInspection) -> instrumentinspection_schema.InstrumentInspection:
    try:
        instrument_inspection = models.Instrumentinspection(**data.dict())
        db_session.add(instrument_inspection)
        db_session.commit()
        return instrumentinspection_schema.InstrumentInspection.from_orm(instrument_inspection)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingInstrumentInspection("Failed creating instrument_inspection.")


def get(db_session: Session, performed_on: str, inspection_datetime: str) -> instrumentinspection_schema.InstrumentInspection:
    try:
        instrument_inspection = db_session.query(models.Instrumentinspection).filter_by(performedOn=performed_on, inspectionDatetime=inspection_datetime).options(joinedload('station')).first()

        if not instrument_inspection:
            raise HTTPException(status_code=404, detail="InstrumentInspection does not exist.")

        return instrumentinspection_schema.InstrumentInspectionWithStationAndInstrument.from_orm(instrument_inspection)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingInstrumentInspection("Failed getting instrument_inspection.")


def query(
    db_session: Session,
    performed_on: str = None,
    inspection_datetime: str = None,
    performed_by: str = None,
    status: str = None,
    remarks: str = None,
    performed_at: str = None,
    limit: int = 25,
    offset: int = 0
) -> List[instrumentinspection_schema.InstrumentInspection]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `instrument_inspection` row skipping
    `offset` number of rows
    """
    try:
        q = db_session.query(models.Instrumentinspection)

        if performed_on is not None:
            q = q.filter_by(performedOn=performed_on)

        if inspection_datetime is not None:
            q = q.filter_by(inspectionDatetime=inspection_datetime)

        if performed_by is not None:
            q = q.filter_by(performedBy=performed_by)

        if status is not None:
            q = q.filter_by(status=status)

        if remarks is not None:
            q = q.filter_by(remarks=remarks)

        if performed_at is not None:
            q = q.filter_by(performedAt=performed_at)

        return [instrumentinspection_schema.InstrumentInspection.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingInstrumentInspectionList("Failed getting instrument_inspection list.")


def update(db_session: Session, performed_on: str, inspection_datetime: str, updates: instrumentinspection_schema.UpdateInstrumentInspection) -> instrumentinspection_schema.InstrumentInspection:
    try:
        db_session.query(models.Instrumentinspection).filter_by(performedOn=performed_on, inspectionDatetime=inspection_datetime).update(updates.dict())
        db_session.commit()
        updated_instrument_inspection = db_session.query(models.Instrumentinspection).filter_by(performedOn=performed_on, inspectionDatetime=inspection_datetime).first()
        return instrumentinspection_schema.InstrumentInspection.from_orm(updated_instrument_inspection)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingInstrumentInspection("Failed updating instrument_inspection")


def delete(db_session: Session, performed_on: str, inspection_datetime: str) -> bool:
    try:
        db_session.query(models.Instrumentinspection).filter_by(performedOn=performed_on, inspectionDatetime=inspection_datetime).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingInstrumentInspection("Failed deleting instrument_inspection.")





import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from apps.climsoft.schemas import faultresolution_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftFaultResolutionService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingFaultResolution(Exception):
    pass


class FailedGettingFaultResolution(Exception):
    pass


class FailedGettingFaultResolutionList(Exception):
    pass


class FailedUpdatingFaultResolution(Exception):
    pass


class FailedDeletingFaultResolution(Exception):
    pass


class FaultResolutionDoesNotExist(Exception):
    pass


def create(db_session: Session, data: faultresolution_schema.CreateFaultResolution) -> faultresolution_schema.FaultResolution:
    try:
        fault_resolution = models.Faultresolution(**data.dict())
        db_session.add(fault_resolution)
        db_session.commit()
        return faultresolution_schema.FaultResolution.from_orm(fault_resolution)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingFaultResolution("Failed creating fault_resolution.")


def get(db_session: Session, resolved_datetime: str, associated_with: str) -> faultresolution_schema.FaultResolution:
    try:
        fault_resolution = db_session.query(models.Faultresolution).filter_by(
            resolvedDatetime=resolved_datetime, 
            associatedWith=associated_with
        ).options(joinedload('instrumentfaultreport')).first()

        if not fault_resolution:
            raise HTTPException(status_code=404, detail="FaultResolution does not exist.")

        return faultresolution_schema.FaultResolutionWithInstrumentFaultReport.from_orm(fault_resolution)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingFaultResolution("Failed getting fault_resolution.")


def query(
    db_session: Session,
    resolved_datetime: str = None,
    associated_with: str = None,
    remarks: str = None,
    resolved_by: str = None,
    limit: int = 25,
    offset: int = 0
) -> List[faultresolution_schema.FaultResolution]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `fault_resolution` row skipping
    `offset` number of rows
    """
    try:
        q = db_session.query(models.Faultresolution)

        if resolved_datetime is not None:
            q = q.filter_by(resolvedDatetime=resolved_datetime)

        if associated_with is not None:
            q = q.filter_by(associatedWith=associated_with)

        if resolved_by is not None:
            q = q.filter_by(resolvedBy=resolved_by)

        if remarks is not None:
            q = q.filter_by(remarks=remarks)

        return [faultresolution_schema.FaultResolution.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingFaultResolutionList("Failed getting fault_resolution list.")


def update(db_session: Session, resolved_datetime: str, associated_with: str, updates: faultresolution_schema.UpdateFaultResolution) -> faultresolution_schema.FaultResolution:
    try:
        db_session.query(models.Faultresolution).filter_by(resolvedDatetime=resolved_datetime, associatedWith=associated_with).update(updates.dict())
        db_session.commit()
        updated_fault_resolution = db_session.query(models.Faultresolution).filter_by(resolvedDatetime=resolved_datetime, associatedWith=associated_with).first()
        return faultresolution_schema.FaultResolution.from_orm(updated_fault_resolution)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingFaultResolution("Failed updating fault_resolution")


def delete(db_session: Session, resolved_datetime: str, associated_with: str) -> bool:
    try:
        db_session.query(models.Faultresolution).filter_by(resolvedDatetime=resolved_datetime, associatedWith=associated_with).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingFaultResolution("Failed deleting fault_resolution.")





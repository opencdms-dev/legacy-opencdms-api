import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import physicalfeature_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftPhysicalFeatureService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingPhysicalFeature(Exception):
    pass


class FailedGettingPhysicalFeature(Exception):
    pass


class FailedGettingPhysicalFeatureList(Exception):
    pass


class FailedUpdatingPhysicalFeature(Exception):
    pass


class FailedDeletingPhysicalFeature(Exception):
    pass


class PhysicalFeatureDoesNotExist(Exception):
    pass


def create(db_session: Session, data: physicalfeature_schema.CreatePhysicalFeature) -> physicalfeature_schema.PhysicalFeature:
    try:
        physical_feature = models.Physicalfeature(**data.dict())
        db_session.add(physical_feature)
        db_session.commit()
        return physicalfeature_schema.PhysicalFeature.from_orm(physical_feature)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingPhysicalFeature("Failed creating physical_feature.")


def get(db_session: Session, performed_on: str, inspection_datetime: str) -> physicalfeature_schema.PhysicalFeature:
    try:
        physical_feature = db_session.query(models.Physicalfeature).filter_by(performedOn=performed_on, inspectionDatetime=inspection_datetime).options(joinedload('station')).first()

        if not physical_feature:
            raise HTTPException(status_code=404, detail="PhysicalFeature does not exist.")

        return physicalfeature_schema.PhysicalFeatureWithStationAndPhysicalFeatureClass.from_orm(physical_feature)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingPhysicalFeature("Failed getting physical_feature.")


def query(
    db_session: Session,
    associated_with: str = None,
    begin_date: str = None,
    end_date: str = None,
    image: str = None,
    description: str = None,
    classified_into: str = None,
    limit: int = 25,
    offset: int = 0
) -> List[physicalfeature_schema.PhysicalFeature]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `physical_feature` row skipping
    `offset` number of rows
    """
    try:
        q = db_session.query(models.Physicalfeature)

        if associated_with is not None:
            q = q.filter_by(associatedWith=associated_with)

        if begin_date is not None:
            q = q.filter_by(beginDate=begin_date)

        if end_date is not None:
            q = q.filter_by(endDate=end_date)

        if image is not None:
            q = q.filter_by(image=image)

        if description is not None:
            q = q.filter_by(description=description)

        if classified_into is not None:
            q = q.filter_by(classifiedInto=classified_into)

        return [physicalfeature_schema.PhysicalFeature.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingPhysicalFeatureList("Failed getting physical_feature list.")


def update(db_session: Session, associated_with: str, begin_date: str, classified_into: str, description: str, updates: physicalfeature_schema.UpdatePhysicalFeature) -> physicalfeature_schema.PhysicalFeature:
    try:
        db_session.query(models.Physicalfeature).filter_by(
            associatedWith=associated_with,
            beginDate=begin_date,
            classifiedInto=classified_into,
            description=description
        ).update(updates.dict())
        db_session.commit()
        updated_physical_feature = db_session.query(models.Physicalfeature).filter_by(
            associatedWith=associated_with,
            beginDate=begin_date,
            classifiedInto=classified_into,
            description=description
        ).first()
        return physicalfeature_schema.PhysicalFeature.from_orm(updated_physical_feature)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingPhysicalFeature("Failed updating physical_feature")


def delete(db_session: Session, associated_with: str, begin_date: str, classified_into: str, description: str) -> bool:
    try:
        db_session.query(models.Physicalfeature).filter_by(
            associatedWith=associated_with,
            beginDate=begin_date,
            classifiedInto=classified_into,
            description=description
        ).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingPhysicalFeature("Failed deleting physical_feature.")





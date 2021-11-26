import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import physicalfeatureclass_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftPhysicalFeatureClassService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingPhysicalFeatureClass(Exception):
    pass


class FailedGettingPhysicalFeatureClass(Exception):
    pass


class FailedGettingPhysicalFeatureClassList(Exception):
    pass


class FailedUpdatingPhysicalFeatureClass(Exception):
    pass


class FailedDeletingPhysicalFeatureClass(Exception):
    pass


class PhysicalFeatureClassDoesNotExist(Exception):
    pass


def create(db_session: Session, data: physicalfeatureclass_schema.CreatePhysicalFeatureClass) -> physicalfeatureclass_schema.PhysicalFeatureClass:
    try:
        physical_feature_class = models.Physicalfeatureclas(**data.dict())
        db_session.add(physical_feature_class)
        db_session.commit()
        return physicalfeatureclass_schema.PhysicalFeatureClass.from_orm(physical_feature_class)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingPhysicalFeatureClass("Failed creating physical_feature_class.")


def get(db_session: Session, belongs_to: str) -> physicalfeatureclass_schema.PhysicalFeatureClass:
    try:
        physical_feature_class = db_session.query(models.Physicalfeatureclas).filter_by(belongsTo=belongs_to).options(joinedload('station')).first()

        if not physical_feature_class:
            raise HTTPException(status_code=404, detail="PhysicalFeatureClass does not exist.")

        return physicalfeatureclass_schema.PhysicalFeatureClassWithStation.from_orm(physical_feature_class)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingPhysicalFeatureClass("Failed getting physical_feature_class.")


def query(
        db_session: Session,
        belongs_to: str = None,
        observed_on: str = None,
        latitude: str = None,
        longitude: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[physicalfeatureclass_schema.PhysicalFeatureClass]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `physical_feature_class` row skipping
    `offset` number of rows
    """
    try:
        q = db_session.query(models.Physicalfeatureclas)

        if belongs_to is not None:
            q = q.filter_by(belongsTo=belongs_to)

        if observed_on is not None:
            q = q.filter_by(observedOn=observed_on)

        if latitude is not None:
            q = q.filter_by(latitude=latitude)

        if longitude is not None:
            q = q.filter_by(longitude=longitude)

        return [physicalfeatureclass_schema.PhysicalFeatureClass.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingPhysicalFeatureClassList("Failed getting physical_feature_class list.")


def update(db_session: Session, belongs_to: str, updates: physicalfeatureclass_schema.UpdatePhysicalFeatureClass) -> physicalfeatureclass_schema.PhysicalFeatureClass:
    try:
        db_session.query(models.Physicalfeatureclas).filter_by(belongsTo=belongs_to).update(updates.dict())
        db_session.commit()
        updated_physical_feature_class = db_session.query(models.Physicalfeatureclas).filter_by(belongsTo=belongs_to).first()
        return physicalfeatureclass_schema.PhysicalFeatureClass.from_orm(updated_physical_feature_class)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingPhysicalFeatureClass("Failed updating physical_feature_class")


def delete(db_session: Session, belongs_to: str) -> bool:
    try:
        db_session.query(models.Physicalfeatureclas).filter_by(belongsTo=belongs_to).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingPhysicalFeatureClass("Failed deleting physical_feature_class.")





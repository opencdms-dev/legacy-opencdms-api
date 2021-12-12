import logging
from typing import List
from sqlalchemy.orm.session import Session
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import acquisitiontype_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftAcquisitionTypeService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingAcquisitionType(Exception):
    pass


class FailedGettingAcquisitionType(Exception):
    pass


class FailedGettingAcquisitionTypeList(Exception):
    pass


class FailedUpdatingAcquisitionType(Exception):
    pass


class FailedDeletingAcquisitionType(Exception):
    pass


class AcquisitionTypeDoesNotExist(Exception):
    pass


def create(db_session: Session, data: acquisitiontype_schema.CreateAcquisitionType) -> acquisitiontype_schema.AcquisitionType:
    try:
        acquisition_type = models.Acquisitiontype(**data.dict())
        db_session.add(acquisition_type)
        db_session.commit()
        return acquisitiontype_schema.AcquisitionType.from_orm(acquisition_type)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingAcquisitionType("Failed creating acquisition_type.")


def get(db_session: Session, code: str) -> acquisitiontype_schema.AcquisitionType:
    try:
        acquisition_type = db_session.query(models.Acquisitiontype).filter_by(code=code).first()

        if not acquisition_type:
            raise HTTPException(status_code=404, detail="AcquisitionType does not exist.")

        return acquisitiontype_schema.AcquisitionType.from_orm(acquisition_type)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingAcquisitionType("Failed getting acquisition_type.")


def query(
        db_session: Session,
        code: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[acquisitiontype_schema.AcquisitionType]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `obselement` row skipping
    `offset` number of rows
    :param db_session:
    :param code:
    :param description:
    :param limit:
    :param offset:
    :return:
    """
    try:
        q = db_session.query(models.Acquisitiontype)

        if code is not None:
            q = q.filter_by(code=code)

        if description is not None:
            q = q.filter(models.Acquisitiontype.description.ilike(f"%{description}%"))

        return [acquisitiontype_schema.AcquisitionType.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingAcquisitionTypeList("Failed getting acquisition_type list.")


def update(db_session: Session, code: str, updates: acquisitiontype_schema.UpdateAcquisitionType) -> acquisitiontype_schema.AcquisitionType:
    try:
        db_session.query(models.Acquisitiontype).filter_by(code=code).update(updates.dict())
        db_session.commit()
        updated_acquisition_type = db_session.query(models.Acquisitiontype).filter_by(code=code).first()
        return acquisitiontype_schema.AcquisitionType.from_orm(updated_acquisition_type)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingAcquisitionType("Failed updating acquisition_type")


def delete(db_session: Session, code: str) -> bool:
    try:
        db_session.query(models.Acquisitiontype).filter_by(code=code).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingAcquisitionType("Failed deleting acquisition_type.")





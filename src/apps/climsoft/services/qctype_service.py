import logging
from typing import List
from sqlalchemy.orm.session import Session
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import qctype_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftQCTypeService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingQCType(Exception):
    pass


class FailedGettingQCType(Exception):
    pass


class FailedGettingQCTypeList(Exception):
    pass


class FailedUpdatingQCType(Exception):
    pass


class FailedDeletingQCType(Exception):
    pass


class QCTypeDoesNotExist(Exception):
    pass


def create(db_session: Session, data: qctype_schema.CreateQCType) -> qctype_schema.QCType:
    try:
        qc_type = models.Qctype(**data.dict())
        db_session.add(qc_type)
        db_session.commit()
        return qctype_schema.QCType.from_orm(qc_type)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingQCType("Failed creating qc_type.")


def get(db_session: Session, code: str) -> qctype_schema.QCType:
    try:
        qc_type = db_session.query(models.Qctype).filter_by(code=code).first()

        if not qc_type:
            raise HTTPException(status_code=404, detail="QCType does not exist.")

        return qctype_schema.QCType.from_orm(qc_type)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingQCType("Failed getting qc_type.")


def query(
        db_session: Session,
        code: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[qctype_schema.QCType]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `qc_types` row skipping
    `offset` number of rows

    """
    try:
        q = db_session.query(models.Qctype)

        if code is not None:
            q = q.filter_by(code=code)

        if description is not None:
            q = q.filter(models.Qctype.description.ilike(f"%{description}%"))

        return [qctype_schema.QCType.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingQCTypeList("Failed getting data form list.")


def update(db_session: Session, code: str, updates: qctype_schema.UpdateQCType) -> qctype_schema.QCType:
    try:
        db_session.query(models.Qctype).filter_by(code=code).update(updates.dict())
        db_session.commit()
        updated_qc_type = db_session.query(models.Qctype).filter_by(code=code).first()
        return qctype_schema.QCType.from_orm(updated_qc_type)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingQCType("Failed updating data form")


def delete(db_session: Session, code: str) -> bool:
    try:
        db_session.query(models.Qctype).filter_by(code=code).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingQCType("Failed deleting data form.")





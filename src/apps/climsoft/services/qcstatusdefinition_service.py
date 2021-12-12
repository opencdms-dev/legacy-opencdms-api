import logging
from typing import List
from sqlalchemy.orm.session import Session
from opencdms.models.climsoft import v4_1_1_core as models
from apps.climsoft.schemas import qcstatusdefinition_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftQCStatusDefinitionService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingQCStatusDefinition(Exception):
    pass


class FailedGettingQCStatusDefinition(Exception):
    pass


class FailedGettingQCStatusDefinitionList(Exception):
    pass


class FailedUpdatingQCStatusDefinition(Exception):
    pass


class FailedDeletingQCStatusDefinition(Exception):
    pass


class QCStatusDefinitionDoesNotExist(Exception):
    pass


def create(db_session: Session, data: qcstatusdefinition_schema.CreateQCStatusDefinition) -> qcstatusdefinition_schema.QCStatusDefinition:
    try:
        qc_status_definition = models.Qcstatusdefinition(**data.dict())
        db_session.add(qc_status_definition)
        db_session.commit()
        return qcstatusdefinition_schema.QCStatusDefinition.from_orm(qc_status_definition)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingQCStatusDefinition("Failed creating qc_status_definition.")


def get(db_session: Session, code: str) -> qcstatusdefinition_schema.QCStatusDefinition:
    try:
        qc_status_definition = db_session.query(models.Qcstatusdefinition).filter_by(code=code).first()

        if not qc_status_definition:
            raise HTTPException(status_code=404, detail="QCStatusDefinition does not exist.")

        return qcstatusdefinition_schema.QCStatusDefinition.from_orm(qc_status_definition)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingQCStatusDefinition("Failed getting qc_status_definition.")


def query(
        db_session: Session,
        code: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[qcstatusdefinition_schema.QCStatusDefinition]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `qc_status_definitions` row skipping
    `offset` number of rows

    """
    try:
        q = db_session.query(models.Qcstatusdefinition)

        if code is not None:
            q = q.filter_by(code=code)

        if description is not None:
            q = q.filter(models.Qcstatusdefinition.description.ilike(f"%{description}%"))

        return [qcstatusdefinition_schema.QCStatusDefinition.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingQCStatusDefinitionList("Failed getting data form list.")


def update(db_session: Session, code: str, updates: qcstatusdefinition_schema.UpdateQCStatusDefinition) -> qcstatusdefinition_schema.QCStatusDefinition:
    try:
        db_session.query(models.Qcstatusdefinition).filter_by(code=code).update(updates.dict())
        db_session.commit()
        updated_qc_status_definition = db_session.query(models.Qcstatusdefinition).filter_by(code=code).first()
        return qcstatusdefinition_schema.QCStatusDefinition.from_orm(updated_qc_status_definition)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingQCStatusDefinition("Failed updating data form")


def delete(db_session: Session, code: str) -> bool:
    try:
        db_session.query(models.Qcstatusdefinition).filter_by(code=code).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingQCStatusDefinition("Failed deleting data form.")





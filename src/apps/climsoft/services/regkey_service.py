import logging
from typing import List
from sqlalchemy.orm.session import Session
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import regkey_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftRegKeyService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingRegKey(Exception):
    pass


class FailedGettingRegKey(Exception):
    pass


class FailedGettingRegKeyList(Exception):
    pass


class FailedUpdatingRegKey(Exception):
    pass


class FailedDeletingRegKey(Exception):
    pass


class RegKeyDoesNotExist(Exception):
    pass


def create(db_session: Session, data: regkey_schema.CreateRegKey) -> regkey_schema.RegKey:
    try:
        reg_key = models.Regkey(**data.dict())
        db_session.add(reg_key)
        db_session.commit()
        return regkey_schema.RegKey.from_orm(reg_key)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingRegKey("Failed creating reg_key.")


def get(db_session: Session, code: str) -> regkey_schema.RegKey:
    try:
        reg_key = db_session.query(models.Regkey).filter_by(code=code).first()

        if not reg_key:
            raise HTTPException(status_code=404, detail="RegKey does not exist.")

        return regkey_schema.RegKey.from_orm(reg_key)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingRegKey("Failed getting reg_key.")


def query(
        db_session: Session,
        key_name: str = None,
        key_value: str = None,
        key_description: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[regkey_schema.RegKey]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `reg_keys` row skipping
    `offset` number of rows

    """
    try:
        q = db_session.query(models.Regkey)

        if key_name is not None:
            q = q.filter_by(keyName=key_name)

        if key_value is not None:
            q = q.filter_by(keyValue=key_value)

        if key_description is not None:
            q = q.filter(models.Regkey.keyDescription.ilike(f"%{key_description}%"))

        return [regkey_schema.RegKey.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingRegKeyList("Failed getting reg key list.")


def update(db_session: Session, code: str, updates: regkey_schema.UpdateRegKey) -> regkey_schema.RegKey:
    try:
        db_session.query(models.Regkey).filter_by(code=code).update(updates.dict())
        db_session.commit()
        updated_reg_key = db_session.query(models.Regkey).filter_by(code=code).first()
        return regkey_schema.RegKey.from_orm(updated_reg_key)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingRegKey("Failed updating reg key")


def delete(db_session: Session, code: str) -> bool:
    try:
        db_session.query(models.Regkey).filter_by(code=code).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingRegKey("Failed deleting reg key.")





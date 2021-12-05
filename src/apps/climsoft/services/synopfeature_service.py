import logging
from typing import List
from sqlalchemy.orm.session import Session
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import synopfeature_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftSynopFeatureService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingSynopFeature(Exception):
    pass


class FailedGettingSynopFeature(Exception):
    pass


class FailedGettingSynopFeatureList(Exception):
    pass


class FailedUpdatingSynopFeature(Exception):
    pass


class FailedDeletingSynopFeature(Exception):
    pass


class SynopFeatureDoesNotExist(Exception):
    pass


def create(db_session: Session, data: synopfeature_schema.CreateSynopFeature) -> synopfeature_schema.SynopFeature:
    try:
        synop_feature = models.Synopfeature(**data.dict())
        db_session.add(synop_feature)
        db_session.commit()
        return synopfeature_schema.SynopFeature.from_orm(synop_feature)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingSynopFeature("Failed creating synop_feature.")


def get(db_session: Session, abbreviation: str) -> synopfeature_schema.SynopFeature:
    try:
        synop_feature = db_session.query(models.Synopfeature).filter_by(abbreviation=abbreviation).first()

        if not synop_feature:
            raise HTTPException(status_code=404, detail="SynopFeature does not exist.")

        return synopfeature_schema.SynopFeature.from_orm(synop_feature)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingSynopFeature("Failed getting synop_feature.")


def query(
        db_session: Session,
        abbreviation: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[synopfeature_schema.SynopFeature]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `synop_features` row skipping
    `offset` number of rows

    """
    try:
        q = db_session.query(models.Synopfeature)

        if abbreviation is not None:
            q = q.filter_by(abbreviation=abbreviation)

        if description is not None:
            q = q.filter(models.Synopfeature.description.ilike(f"%{description}%"))

        return [synopfeature_schema.SynopFeature.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingSynopFeatureList("Failed getting synop feature list.")


def update(db_session: Session, abbreviation: str, updates: synopfeature_schema.UpdateSynopFeature) -> synopfeature_schema.SynopFeature:
    try:
        db_session.query(models.Synopfeature).filter_by(abbreviation=abbreviation).update(updates.dict())
        db_session.commit()
        updated_synop_feature = db_session.query(models.Synopfeature).filter_by(abbreviation=abbreviation).first()
        return synopfeature_schema.SynopFeature.from_orm(updated_synop_feature)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingSynopFeature("Failed updating synop feature")


def delete(db_session: Session, abbreviation: str) -> bool:
    try:
        db_session.query(models.Synopfeature).filter_by(abbreviation=abbreviation).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingSynopFeature("Failed deleting synop feature.")





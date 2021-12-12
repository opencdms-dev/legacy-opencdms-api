import logging
from typing import List
from sqlalchemy.orm.session import Session
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import obselement_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftObsElementService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingObsElement(Exception):
    pass


class FailedGettingObsElement(Exception):
    pass


class FailedGettingObsElementList(Exception):
    pass


class FailedUpdatingObsElement(Exception):
    pass


class FailedDeletingObsElement(Exception):
    pass


class ObsElementDoesNotExist(Exception):
    pass


def create(db_session: Session, data: obselement_schema.CreateObsElement) -> obselement_schema.ObsElement:
    try:
        obs_element = models.Obselement(**data.dict())
        db_session.add(obs_element)
        db_session.commit()
        return obselement_schema.ObsElement.from_orm(obs_element)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingObsElement("Failed creating obs_element.")


def get(db_session: Session, element_id: str) -> obselement_schema.ObsElement:
    try:
        obs_element = db_session.query(models.Obselement).filter_by(elementId=element_id).first()

        if not obs_element:
            raise HTTPException(status_code=404, detail="ObsElement does not exist.")

        return obselement_schema.ObsElement.from_orm(obs_element)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingObsElement("Failed getting obs_element.")


def query(
        db_session: Session,
        element_id: str = None,
        element_name: str = None,
        abbreviation: str = None,
        description: str = None,
        element_scale: float = None,
        upper_limit: float = None,
        lower_limit: str = None,
        units: str = None,
        element_type: str = None,
        qc_total_required: int = None,
        selected: bool = None,
        limit: int = 25,
        offset: int = 0
) -> List[obselement_schema.ObsElement]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `obselement` row skipping
    `offset` number of rows

    :param db_session: sqlalchemy database session
    :param element_id: compares with `elementId` column for an exact match
    :param element_name: compares with `elementName` column for an exact match
    :param abbreviation: compares with `abbreviation` column for an exact match
    :param description: check if `description` column contains given value
    :param element_scale: returns items with equal or greater element scale
    :param upper_limit: returns items with lower or equal upper limit
    :param lower_limit: returns items with higher or equal lower limit
    :param units: checks if `units` column contains given value
    :param element_type: checks if `elementtype` column contains given value
    :param qc_total_required: returns items with greater or equal qcTotalRequired
    :param selected: compares with `selected` column for an exact match
    :param limit: describes page size
    :param offset: describe how many to skip
    :return: list of `obselement`
    """
    try:
        q = db_session.query(models.Obselement)

        if element_id is not None:
            q = q.filter_by(elementId=element_id)

        if element_name is not None:
            q = q.filter_by(elementName=element_name)

        if abbreviation is not None:
            q = q.filter_by(abbreviation=abbreviation)

        if description is not None:
            q = q.filter(models.Obselement.description.ilike(f"%{description}%"))

        if element_scale is not None:
            q = q.filter(models.Obselement.elementScale >= element_scale)

        if upper_limit is not None:
            q = q.filter(models.Obselement.upperLimit <= upper_limit)

        if lower_limit is not None:
            q = q.filter(models.Obselement.lowerLimit >= lower_limit)

        if units is not None:
            q = q.filter(models.Obselement.units.ilike(f"%{units}%"))

        if element_type is not None:
            q = q.filter(models.Obselement.elementtype.ilike(f"%{element_type}%"))

        if qc_total_required is not None:
            q = q.filter(models.Obselement.qcTotalRequired >= qc_total_required)

        if selected is not None:
            q = q.filter_by(selected=selected)

        return [obselement_schema.ObsElement.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingObsElementList("Failed getting obs_element list.")


def update(db_session: Session, element_id: str, updates: obselement_schema.UpdateObsElement) -> obselement_schema.ObsElement:
    try:
        db_session.query(models.Obselement).filter_by(elementId=element_id).update(updates.dict())
        db_session.commit()
        updated_obs_element = db_session.query(models.Obselement).filter_by(elementId=element_id).first()
        return obselement_schema.ObsElement.from_orm(updated_obs_element)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingObsElement("Failed updating obs_element")


def delete(db_session: Session, element_id: str) -> bool:
    try:
        db_session.query(models.Obselement).filter_by(elementId=element_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingObsElement("Failed deleting obs_element.")





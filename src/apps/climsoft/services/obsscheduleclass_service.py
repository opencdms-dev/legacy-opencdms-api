import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from apps.climsoft.schemas import obsscheduleclass_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftObsScheduleClassService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingObsScheduleClass(Exception):
    pass


class FailedGettingObsScheduleClass(Exception):
    pass


class FailedGettingObsScheduleClassList(Exception):
    pass


class FailedUpdatingObsScheduleClass(Exception):
    pass


class FailedDeletingObsScheduleClass(Exception):
    pass


class ObsScheduleClassDoesNotExist(Exception):
    pass


def create(db_session: Session, data: obsscheduleclass_schema.CreateObsScheduleClass) -> obsscheduleclass_schema.ObsScheduleClass:
    try:
        obs_schedule_class = models.Obsscheduleclas(**data.dict())
        db_session.add(obs_schedule_class)
        db_session.commit()
        return obsscheduleclass_schema.ObsScheduleClass.from_orm(obs_schedule_class)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingObsScheduleClass("Failed creating obs_schedule_class.")


def get(db_session: Session, schedule_class: str) -> obsscheduleclass_schema.ObsScheduleClass:
    try:
        obs_schedule_class = db_session.query(models.Obsscheduleclas).filter_by(scheduleClass=schedule_class).options(joinedload('station')).first()

        if not obs_schedule_class:
            raise HTTPException(status_code=404, detail="ObsScheduleClass does not exist.")

        return obsscheduleclass_schema.ObsScheduleClassWithStation.from_orm(obs_schedule_class)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingObsScheduleClass("Failed getting obs_schedule_class.")


def query(
        db_session: Session,
        schedule_class: str = None,
        description: str = None,
        refers_to: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[obsscheduleclass_schema.ObsScheduleClass]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `obs_schedule_class` row skipping
    `offset` number of rows
    :param db_session: database session
    :param schedule_class: filter by primary key
    :param description: checks if description column contains given input
    :param refers_to: filter by station id
    :param limit: returns `limit` number of records
    :param offset: skips `offset` number of records
    :return: list of obsscheduleclass
    """
    try:
        q = db_session.query(models.Obsscheduleclas)

        if schedule_class is not None:
            q = q.filter_by(scheduleClass=schedule_class)

        if description is not None:
            q = q.filter(models.Obsscheduleclas.description.ilike(f"%{description}%"))

        if refers_to is not None:
            q = q.filter_by(refersTo=refers_to)

        return [obsscheduleclass_schema.ObsScheduleClass.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingObsScheduleClassList("Failed getting obs_schedule_class list.")


def update(db_session: Session, schedule_class: str, updates: obsscheduleclass_schema.UpdateObsScheduleClass) -> obsscheduleclass_schema.ObsScheduleClass:
    try:
        db_session.query(models.Obsscheduleclas).filter_by(scheduleClass=schedule_class).update(updates.dict())
        db_session.commit()
        updated_obs_schedule_class = db_session.query(models.Obsscheduleclas).filter_by(scheduleClass=schedule_class).first()
        return obsscheduleclass_schema.ObsScheduleClass.from_orm(updated_obs_schedule_class)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingObsScheduleClass("Failed updating obs_schedule_class")


def delete(db_session: Session, schedule_class: str) -> bool:
    try:
        db_session.query(models.Obsscheduleclas).filter_by(scheduleClass=schedule_class).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingObsScheduleClass("Failed deleting obs_schedule_class.")





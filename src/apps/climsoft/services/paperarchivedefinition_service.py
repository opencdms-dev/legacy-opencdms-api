import logging
from typing import List
from sqlalchemy.orm.session import Session
from opencdms.models.climsoft import v4_1_1_core as models
from apps.climsoft.schemas import paperarchivedefinition_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftPaperArchiveDefinitionService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingPaperArchiveDefinition(Exception):
    pass


class FailedGettingPaperArchiveDefinition(Exception):
    pass


class FailedGettingPaperArchiveDefinitionList(Exception):
    pass


class FailedUpdatingPaperArchiveDefinition(Exception):
    pass


class FailedDeletingPaperArchiveDefinition(Exception):
    pass


class PaperArchiveDefinitionDoesNotExist(Exception):
    pass


def create(db_session: Session, data: paperarchivedefinition_schema.CreatePaperArchiveDefinition) -> paperarchivedefinition_schema.PaperArchiveDefinition:
    try:
        paper_archive_definition = models.Paperarchivedefinition(**data.dict())
        db_session.add(paper_archive_definition)
        db_session.commit()
        return paperarchivedefinition_schema.PaperArchiveDefinition.from_orm(paper_archive_definition)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingPaperArchiveDefinition("Failed creating paper_archive_definition.")


def get(db_session: Session, form_id: str) -> paperarchivedefinition_schema.PaperArchiveDefinition:
    try:
        paper_archive_definition = db_session.query(models.Paperarchivedefinition).filter_by(formId=form_id).first()

        if not paper_archive_definition:
            raise HTTPException(status_code=404, detail="PaperArchiveDefinition does not exist.")

        return paperarchivedefinition_schema.PaperArchiveDefinition.from_orm(paper_archive_definition)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingPaperArchiveDefinition("Failed getting paper_archive_definition.")


def query(
        db_session: Session,
        form_id: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0
) -> List[paperarchivedefinition_schema.PaperArchiveDefinition]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `paper_archive_definitions` row skipping
    `offset` number of rows

    """
    try:
        q = db_session.query(models.Paperarchivedefinition)

        if form_id is not None:
            q = q.filter_by(formId=form_id)

        if description is not None:
            q = q.filter(models.Paperarchivedefinition.description.ilike(f"%{description}%"))

        return [paperarchivedefinition_schema.PaperArchiveDefinition.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingPaperArchiveDefinitionList("Failed getting data form list.")


def update(db_session: Session, form_id: str, updates: paperarchivedefinition_schema.UpdatePaperArchiveDefinition) -> paperarchivedefinition_schema.PaperArchiveDefinition:
    try:
        db_session.query(models.Paperarchivedefinition).filter_by(formId=form_id).update(updates.dict())
        db_session.commit()
        updated_paper_archive_definition = db_session.query(models.Paperarchivedefinition).filter_by(formId=form_id).first()
        return paperarchivedefinition_schema.PaperArchiveDefinition.from_orm(updated_paper_archive_definition)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingPaperArchiveDefinition("Failed updating data form")


def delete(db_session: Session, form_id: str) -> bool:
    try:
        db_session.query(models.Paperarchivedefinition).filter_by(formId=form_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingPaperArchiveDefinition("Failed deleting data form.")





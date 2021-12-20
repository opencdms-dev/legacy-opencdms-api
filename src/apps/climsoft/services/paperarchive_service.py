import logging
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from apps.climsoft.schemas import paperarchive_schema
from opencdms.models.climsoft import v4_1_1_core as models


logger = logging.getLogger("ClimsoftPaperArchiveService")
logging.basicConfig(level=logging.INFO)


class FailedGettingPaperArchive(Exception):
    pass


class FailedFetchingPaperArchives(Exception):
    pass


class FailedCreatingPaperArchive(Exception):
    pass


class FailedUpdatingPaperArchive(Exception):
    pass


class FailedDeletingPaperArchive(Exception):
    pass


class FailedGettingPaperArchiveList(Exception):
    pass


def query(
    db_session: Session,
    belongs_to: str = None,
    form_datetime: str = None,
    image: str = None,
    classified_into: str = None,
    offset: int = 0,
    limit: int = 25
):
    try:
        q = db_session.query(models.Paperarchive)

        if belongs_to is not None:
            q = q.filter_by(belongsTo=belongs_to)

        if form_datetime is not None:
            q = q.filter_by(formDatetime=form_datetime)

        if image is not None:
            q = q.filter_by(image=image)

        if classified_into is not None:
            q = q.filter_by(classifiedInto=classified_into)

        return [paperarchive_schema.PaperArchive.from_orm(paper_archive) for paper_archive in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedFetchingPaperArchives("Failed fetching paper archive.")


def get(db_session: Session, belongs_to: str, form_datetime: str, classified_into: str):
    try:
        response = db_session.query(models.Paperarchive).filter_by(
            belongsTo=belongs_to,
            formDatetime=form_datetime,
            classifiedInto=classified_into
        ) \
            .options(joinedload("station"), joinedload("paperarchivedefinition")) \
            .first()
        if not response:
            raise HTTPException(status_code=404, detail="Paper archive not found.")

        return paperarchive_schema.PaperArchiveWithStationAndPaperArchiveDefinition.from_orm(response)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingPaperArchive("Failed getting paper archive.")


def create(db_session: Session, data: paperarchive_schema.CreatePaperArchive):
    try:
        paper_archive = models.Paperarchive(
            **data.dict()
        )
        db_session.add(paper_archive)
        db_session.commit()
        return paperarchive_schema.PaperArchive.from_orm(paper_archive)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingPaperArchive("Failed creating paper archive.")


def update(
    db_session: Session,
    belongs_to: str,
    form_datetime: str,
    classified_into: str,
    data: paperarchive_schema.UpdatePaperArchive
):
    try:
        db_session.query(models.Paperarchive).filter_by(
            belongsTo=belongs_to,
            formDatetime=form_datetime,
            classifiedInto=classified_into
        ).update(data.dict())
        db_session.commit()
        updated_paper_archive = db_session.query(models.Paperarchive).filter_by(
            belongsTo=belongs_to,
            formDatetime=form_datetime,
            classifiedInto=classified_into
        ).first()
        return paperarchive_schema.PaperArchive.from_orm(updated_paper_archive)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingPaperArchive("Failed updating paper archive.")


def delete(
    db_session: Session,
    belongs_to: str,
    form_datetime: str,
    classified_into: str
):
    try:
        db_session.query(models.Paperarchive).filter_by(
            belongsTo=belongs_to,
            formDatetime=form_datetime,
            classifiedInto=classified_into
        ).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingPaperArchive("Failed deleting paper archive.")

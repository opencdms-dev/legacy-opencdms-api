from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from src.apps.climsoft.schemas import paperarchive_schema
from opencdms.models.climsoft import v4_1_1_core as models


class FailedGettingPaperArchive(Exception):
    pass


def get(db_session: Session, belongs_to: str, from_datetime: str, classified_info: str):
    try:
        response = db_session.query(models.Paperarchive).filter_by(
            belongsTp=belongs_to,
            fromDatetime=from_datetime,
            classifiedInfo=classified_info
        ) \
            .options(joinedload("station"), joinedload("paperarchivedefinition")) \
            .first()

        return paperarchive_schema.PaperArchiveWithStationAndPaperArchiveDefinition.from_orm(response)
    except Exception as e:
        raise FailedGettingPaperArchive("Failed getting paper archive.")

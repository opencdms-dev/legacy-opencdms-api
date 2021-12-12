import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import instrumentfaultreport_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftInstrumentFaultReportService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingInstrumentFaultReport(Exception):
    pass


class FailedGettingInstrumentFaultReport(Exception):
    pass


class FailedGettingInstrumentFaultReportList(Exception):
    pass


class FailedUpdatingInstrumentFaultReport(Exception):
    pass


class FailedDeletingInstrumentFaultReport(Exception):
    pass


class InstrumentFaultReportDoesNotExist(Exception):
    pass


def create(db_session: Session, data: instrumentfaultreport_schema.CreateInstrumentFaultReport) -> instrumentfaultreport_schema.InstrumentFaultReport:
    try:
        instrument_fault_report = models.Instrumentfaultreport(**data.dict())
        db_session.add(instrument_fault_report)
        db_session.commit()
        return instrumentfaultreport_schema.InstrumentFaultReport.from_orm(instrument_fault_report)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingInstrumentFaultReport("Failed creating instrument_fault_report.")


def get(db_session: Session, report_id: int) -> instrumentfaultreport_schema.InstrumentFaultReport:
    try:
        instrument_fault_report = db_session.query(models.Instrumentfaultreport).filter_by(reportId=report_id).options(joinedload('station')).first()

        if not instrument_fault_report:
            raise HTTPException(status_code=404, detail="InstrumentFaultReport does not exist.")

        return instrumentfaultreport_schema.InstrumentFaultReportWithStationAndInstrument.from_orm(instrument_fault_report)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingInstrumentFaultReport("Failed getting instrument_fault_report.")


def query(
    db_session: Session,
    refers_to: str = None,
    report_id: str = None,
    report_datetime: str = None,
    fault_description: float = None,
    reported_by: str = None,
    received_datetime: str = None,
    received_by: float = None,
    reported_from: float = None,
    limit: int = 25,
    offset: int = 0
) -> List[instrumentfaultreport_schema.InstrumentFaultReport]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `instrument_fault_report` row skipping
    `offset` number of rows
    """
    try:
        q = db_session.query(models.Instrumentfaultreport)

        if refers_to is not None:
            q = q.filter_by(refersTo=refers_to)

        if report_id is not None:
            q = q.filter_by(reportId=report_id)

        if report_datetime is not None:
            q = q.filter_by(reportDatetime=report_datetime)

        if fault_description is not None:
            q = q.filter_by(faultDescription=fault_description)

        if reported_by is not None:
            q = q.filter_by(reportedBy=reported_by)

        if received_datetime is not None:
            q = q.filter_by(receivedDatetime=received_datetime)

        if received_by is not None:
            q = q.filter_by(receivedBy=received_by)

        if reported_from is not None:
            q = q.filter_by(reportedFrom=reported_from)

        return [instrumentfaultreport_schema.InstrumentFaultReport.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingInstrumentFaultReportList("Failed getting instrument_fault_report list.")


def update(db_session: Session, report_id: int, updates: instrumentfaultreport_schema.UpdateInstrumentFaultReport) -> instrumentfaultreport_schema.InstrumentFaultReport:
    try:
        db_session.query(models.Instrumentfaultreport).filter_by(reportId=report_id).update(updates.dict())
        db_session.commit()
        updated_instrument_fault_report = db_session.query(models.Instrumentfaultreport).filter_by(reportId=report_id).first()
        return instrumentfaultreport_schema.InstrumentFaultReport.from_orm(updated_instrument_fault_report)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingInstrumentFaultReport("Failed updating instrument_fault_report")


def delete(db_session: Session, report_id: int) -> bool:
    try:
        db_session.query(models.Instrumentfaultreport).filter_by(reportId=report_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingInstrumentFaultReport("Failed deleting instrument_fault_report.")





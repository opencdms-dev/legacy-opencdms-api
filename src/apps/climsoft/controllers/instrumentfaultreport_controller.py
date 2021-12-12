from fastapi import APIRouter, Depends
from apps.climsoft.services import instrumentfaultreport_service
from apps.climsoft.schemas import instrumentfaultreport_schema
from utils.response import get_success_response, get_error_response
from apps.climsoft.db.engine import SessionLocal
from sqlalchemy.orm.session import Session
from dependencies import auth


router = APIRouter(
    prefix="/api/climsoft/v1",
    tags=["climsoft"],
    dependencies=[Depends(auth.get_current_user)]
)


async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/instrument-fault-reports", response_model=instrumentfaultreport_schema.InstrumentFaultReportResponse)
def get_instrument_fault_report(
    refers_to: str = None,
    report_id: str = None,
    report_datetime: str = None,
    fault_description: float = None,
    reported_by: str = None,
    received_datetime: str = None,
    received_by: float = None,
    reported_from: float = None,
    limit: int = 25,
    offset: int = 0,
    db_session: Session = Depends(get_db)
):
    try:
        instrument_fault_report = instrumentfaultreport_service.query(
            db_session=db_session,
            refers_to=refers_to,
            report_id=report_id,
            report_datetime=report_datetime,
            fault_description=fault_description,
            reported_by=reported_by,
            received_datetime=received_datetime,
            received_by=received_by,
            reported_from=reported_from,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=instrument_fault_report, message="Successfully fetched instrument_fault_report.")
    except instrumentfaultreport_service.FailedGettingInstrumentFaultReportList as e:
        return get_error_response(message=str(e))


@router.get("/instrument-fault-reports/{report_id}", response_model=instrumentfaultreport_schema.InstrumentFaultReportWithStationAndInstrumentResponse)
def get_instrument_fault_report_by_id(report_id: int, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[instrumentfaultreport_service.get(db_session=db_session, report_id=report_id)],
            message="Successfully fetched instrument_fault_report."
        )
    except instrumentfaultreport_service.FailedGettingInstrumentFaultReport as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/instrument-fault-reports", response_model=instrumentfaultreport_schema.InstrumentFaultReportResponse)
def create_instrument_fault_report(data: instrumentfaultreport_schema.CreateInstrumentFaultReport, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[instrumentfaultreport_service.create(db_session=db_session, data=data)],
            message="Successfully created instrument_fault_report."
        )
    except instrumentfaultreport_service.FailedCreatingInstrumentFaultReport as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/instrument-fault-reports/{report_id}", response_model=instrumentfaultreport_schema.InstrumentFaultReportResponse)
def update_instrument_fault_report(report_id: int, data: instrumentfaultreport_schema.UpdateInstrumentFaultReport, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[instrumentfaultreport_service.update(db_session=db_session, report_id=report_id, updates=data)],
            message="Successfully updated instrument_fault_report."
        )
    except instrumentfaultreport_service.FailedUpdatingInstrumentFaultReport as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/instrument-fault-reports/{report_id}", response_model=instrumentfaultreport_schema.InstrumentFaultReportResponse)
def delete_instrument_fault_report(report_id: int, db_session: Session = Depends(get_db)):
    try:
        instrumentfaultreport_service.delete(db_session=db_session, report_id=report_id)
        return get_success_response(
            result=[],
            message="Successfully deleted instrument_fault_report."
        )
    except instrumentfaultreport_service.FailedDeletingInstrumentFaultReport as e:
        return get_error_response(
            message=str(e)
        )






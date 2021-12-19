from fastapi import APIRouter, Depends
from apps.climsoft.services import instrument_service
from apps.climsoft.schemas import instrument_schema
from utils.response import get_success_response, get_error_response
from apps.climsoft.db.engine import SessionLocal
from sqlalchemy.orm.session import Session
from dependencies import auth


router = APIRouter(
    prefix="/v1",
    tags=["climsoft"],
    dependencies=[Depends(auth.get_current_user)]
)


async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/instruments", response_model=instrument_schema.InstrumentResponse)
def get_instruments(
        instrument_id: str = None,
        instrument_name: str = None,
        serial_number: str = None,
        abbreviation: str = None,
        model: str = None,
        manufacturer: str = None,
        instrument_uncertainty: float = None,
        installation_datetime: str = None,
        uninstallation_datetime: str = None,
        height: str = None,
        station_id: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        instruments = instrument_service.query(
            db_session=db_session,
            instrument_id=instrument_id,
            instrument_name=instrument_name,
            serial_number=serial_number,
            abbreviation=abbreviation,
            model=model,
            manufacturer=manufacturer,
            instrument_uncertainty=instrument_uncertainty,
            installation_datetime=installation_datetime,
            uninstallation_datetime=uninstallation_datetime,
            height=height,
            station_id=station_id,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=instruments, message="Successfully fetched instruments.")
    except instrument_service.FailedGettingInstrumentList as e:
        return get_error_response(message=str(e))


@router.get("/instruments/{instrument_id}", response_model=instrument_schema.InstrumentWithStationResponse)
def get_instrument_by_id(instrument_id: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[instrument_service.get(db_session=db_session, instrument_id=instrument_id)],
            message="Successfully fetched instrument."
        )
    except instrument_service.FailedGettingInstrument as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/instruments", response_model=instrument_schema.InstrumentResponse)
def create_instrument(data: instrument_schema.CreateInstrument, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[instrument_service.create(db_session=db_session, data=data)],
            message="Successfully created instrument."
        )
    except instrument_service.FailedCreatingInstrument as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/instruments/{instrument_id}", response_model=instrument_schema.InstrumentResponse)
def update_instrument(instrument_id: str, data: instrument_schema.UpdateInstrument, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[instrument_service.update(db_session=db_session, instrument_id=instrument_id, updates=data)],
            message="Successfully updated instrument."
        )
    except instrument_service.FailedUpdatingInstrument as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/instruments/{instrument_id}", response_model=instrument_schema.InstrumentResponse)
def delete_instrument(instrument_id: str, db_session: Session = Depends(get_db)):
    try:
        instrument_service.delete(db_session=db_session, instrument_id=instrument_id)
        return get_success_response(
            result=[],
            message="Successfully deleted instrument."
        )
    except instrument_service.FailedDeletingInstrument as e:
        return get_error_response(
            message=str(e)
        )






from fastapi import APIRouter, Depends
from apps.climsoft.services import stationqualifier_service
from apps.climsoft.schemas import stationqualifier_schema
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


@router.get("/station-qualifiers", response_model=stationqualifier_schema.StationQualifierResponse)
def get_station_qualifier(
    qualifier: str = None,
    qualifier_begin_date: str = None,
    qualifier_end_date: str = None,
    station_timezone: int = None,
    station_network_type: str = None,
    belongs_to: str = None,
    limit: int = 25,
    offset: int = 0,
    db_session: Session = Depends(get_db)
):
    try:
        station_qualifier = stationqualifier_service.query(
            db_session=db_session,
            belongs_to=belongs_to,
            qualifier=qualifier,
            qualifier_begin_date=qualifier_begin_date,
            qualifier_end_date=qualifier_end_date,
            station_timezone=station_timezone,
            station_network_type=station_network_type,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=station_qualifier, message="Successfully fetched station_qualifier.")
    except stationqualifier_service.FailedGettingStationQualifierList as e:
        return get_error_response(message=str(e))


@router.get("/station-qualifiers/{qualifier}/{qualifier_begin_date}/{qualifier_end_date}/{belongs_to}", response_model=stationqualifier_schema.StationQualifierWithStationResponse)
def get_station_qualifier_by_id(qualifier: str, qualifier_begin_date: str, qualifier_end_date: str, belongs_to: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[stationqualifier_service.get(
                db_session=db_session,
                qualifier=qualifier,
                qualifier_begin_date=qualifier_begin_date,
                qualifier_end_date=qualifier_end_date,
                belongs_to=belongs_to
            )],
            message="Successfully fetched station_qualifier."
        )
    except stationqualifier_service.FailedGettingStationQualifier as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/station-qualifiers", response_model=stationqualifier_schema.StationQualifierResponse)
def create_station_qualifier(data: stationqualifier_schema.CreateStationQualifier, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[stationqualifier_service.create(db_session=db_session, data=data)],
            message="Successfully created station_qualifier."
        )
    except stationqualifier_service.FailedCreatingStationQualifier as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/station-qualifiers/{qualifier}/{qualifier_begin_date}/{qualifier_end_date}/{belongs_to}", response_model=stationqualifier_schema.StationQualifierResponse)
def update_station_qualifier(qualifier: str, qualifier_begin_date: str, qualifier_end_date: str, belongs_to: str, data: stationqualifier_schema.UpdateStationQualifier, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[stationqualifier_service.update(
                db_session=db_session,
                qualifier=qualifier,
                qualifier_begin_date=qualifier_begin_date,
                qualifier_end_date=qualifier_end_date,
                belongs_to=belongs_to,
                updates=data
            )],
            message="Successfully updated station_qualifier."
        )
    except stationqualifier_service.FailedUpdatingStationQualifier as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/station-qualifiers/{qualifier}/{qualifier_begin_date}/{qualifier_end_date}/{belongs_to}", response_model=stationqualifier_schema.StationQualifierResponse)
def delete_station_qualifier(qualifier: str, qualifier_begin_date: str, qualifier_end_date: str, belongs_to: str, db_session: Session = Depends(get_db)):
    try:
        stationqualifier_service.delete(
            db_session=db_session,
            qualifier=qualifier,
            qualifier_begin_date=qualifier_begin_date,
            qualifier_end_date=qualifier_end_date,
            belongs_to=belongs_to
        )
        return get_success_response(
            result=[],
            message="Successfully deleted station_qualifier."
        )
    except stationqualifier_service.FailedDeletingStationQualifier as e:
        return get_error_response(
            message=str(e)
        )






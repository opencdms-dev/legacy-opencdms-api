from fastapi import APIRouter, Depends
from apps.climsoft.services import obsscheduleclass_service
from apps.climsoft.schemas import obsscheduleclass_schema
from utils.response import get_success_response, get_error_response
from sqlalchemy.orm.session import Session
from apps.climsoft.db.engine import SessionLocal
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


@router.get("/obs-schedule-class", response_model=obsscheduleclass_schema.ObsScheduleClassResponse)
def get_obs_schedule_class(
        schedule_class: str = None,
        description: str = None,
        refers_to: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        obs_schedule_class = obsscheduleclass_service.query(
            db_session=db_session,
            schedule_class=schedule_class,
            description=description,
            refers_to=refers_to,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=obs_schedule_class, message="Successfully fetched obs_schedule_class.")
    except obsscheduleclass_service.FailedGettingObsScheduleClassList as e:
        return get_error_response(message=str(e))


@router.get("/obs-schedule-class/{schedule_class}", response_model=obsscheduleclass_schema.ObsScheduleClassWithStationResponse)
def get_instrument_by_id(schedule_class: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[obsscheduleclass_service.get(db_session=db_session, schedule_class=schedule_class)],
            message="Successfully fetched instrument."
        )
    except obsscheduleclass_service.FailedGettingObsScheduleClass as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/obs-schedule-class", response_model=obsscheduleclass_schema.ObsScheduleClassResponse)
def create_instrument(data: obsscheduleclass_schema.CreateObsScheduleClass, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[obsscheduleclass_service.create(db_session=db_session, data=data)],
            message="Successfully created instrument."
        )
    except obsscheduleclass_service.FailedCreatingObsScheduleClass as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/obs-schedule-class/{schedule_class}", response_model=obsscheduleclass_schema.ObsScheduleClassResponse)
def update_instrument(schedule_class: str, data: obsscheduleclass_schema.UpdateObsScheduleClass, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[obsscheduleclass_service.update(db_session=db_session, schedule_class=schedule_class, updates=data)],
            message="Successfully updated instrument."
        )
    except obsscheduleclass_service.FailedUpdatingObsScheduleClass as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/obs-schedule-class/{schedule_class}", response_model=obsscheduleclass_schema.ObsScheduleClassResponse)
def delete_instrument(schedule_class: str, db_session: Session = Depends(get_db)):
    try:
        obsscheduleclass_service.delete(db_session=db_session, schedule_class=schedule_class)
        return get_success_response(
            result=[],
            message="Successfully deleted instrument."
        )
    except obsscheduleclass_service.FailedDeletingObsScheduleClass as e:
        return get_error_response(
            message=str(e)
        )






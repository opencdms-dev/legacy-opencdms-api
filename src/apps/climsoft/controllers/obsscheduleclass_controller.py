from fastapi import APIRouter
from fastapi_sqlalchemy import db
from src.apps.climsoft.services import obsscheduleclass_service
from src.apps.climsoft.schemas import obsscheduleclass_schema
from src.utils.response import get_success_response, get_error_response


router = APIRouter(
    prefix="/api/v1/climsoft",
    tags=["climsoft"]
)


@router.get("/obs-schedule-class", response_model=obsscheduleclass_schema.ObsScheduleClassResponse)
def get_obs_schedule_class(
        schedule_class: str = None,
        description: str = None,
        refers_to: str = None,
        limit: int = 25,
        offset: int = 0
):
    try:
        obs_schedule_class = obsscheduleclass_service.query(
            db_session=db.session,
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
def get_instrument_by_id(schedule_class: str):
    try:
        return get_success_response(
            result=[obsscheduleclass_service.get(db_session=db.session, schedule_class=schedule_class)],
            message="Successfully fetched instrument."
        )
    except obsscheduleclass_service.FailedGettingObsScheduleClass as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/obs-schedule-class", response_model=obsscheduleclass_schema.ObsScheduleClassResponse)
def create_instrument(data: obsscheduleclass_schema.CreateObsScheduleClass):
    try:
        return get_success_response(
            result=[obsscheduleclass_service.create(db_session=db.session, data=data)],
            message="Successfully created instrument."
        )
    except obsscheduleclass_service.FailedCreatingObsScheduleClass as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/obs-schedule-class/{schedule_class}", response_model=obsscheduleclass_schema.ObsScheduleClassResponse)
def update_instrument(schedule_class: str, data: obsscheduleclass_schema.UpdateObsScheduleClass):
    try:
        return get_success_response(
            result=[obsscheduleclass_service.update(db_session=db.session, schedule_class=schedule_class, updates=data)],
            message="Successfully updated instrument."
        )
    except obsscheduleclass_service.FailedUpdatingObsScheduleClass as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/obs-schedule-class/{schedule_class}", response_model=obsscheduleclass_schema.ObsScheduleClassResponse)
def delete_instrument(schedule_class: str):
    try:
        obsscheduleclass_service.delete(db_session=db.session, schedule_class=schedule_class)
        return get_success_response(
            result=[],
            message="Successfully deleted instrument."
        )
    except obsscheduleclass_service.FailedDeletingObsScheduleClass as e:
        return get_error_response(
            message=str(e)
        )






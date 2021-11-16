from fastapi import APIRouter
from fastapi_sqlalchemy import db
from src.apps.climsoft.services import observationinitial_service
from src.apps.climsoft.schemas import observationinitial_schema
from src.utils.response import get_success_response, get_error_response


router = APIRouter(
    prefix="/api/v1/climsoft",
    tags=["climsoft"]
)


@router.get("/observation-initial", response_model=observationinitial_schema.ObservationInitialResponse)
def get_observation_initials(
        recorded_from: str = None,
        described_by: int = None,
        obs_datetime: str = None,
        qc_status: int = None,
        acquisition_type: int = None,
        obs_level: int = None,
        obs_value: float = None,
        flag: str = None,
        period: int = None,
        qc_type_log: str = None,
        data_form: str = None,
        captured_by: str = None,
        mark: bool = None,
        temperature_units: str = None,
        precipitation_units: str = None,
        vis_units: str = None,
        data_source_timezone: int = None,
        limit: int = 25,
        offset: int = 0
):
    try:
        observation_initials = observationinitial_service.query(
            db_session=db.session,
            recorded_from=recorded_from,
            obs_datetime=obs_datetime,
            qc_status=qc_status,
            described_by=described_by,
            acquisition_type=acquisition_type,
            obs_value=obs_value,
            obs_level=obs_level,
            flag=flag,
            period=period,
            qc_type_log=qc_type_log,
            data_form=data_form,
            captured_by=captured_by,
            mark=mark,
            temperature_units=temperature_units,
            precipitation_units=precipitation_units,
            vis_units=vis_units,
            data_source_timezone=data_source_timezone,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=observation_initials, message="Successfully fetched observation_initials.")
    except observationinitial_service.FailedGettingObservationInitialList as e:
        return get_error_response(message=str(e))


@router.get("/observation-initial/{recorded_from}/{described_by}/{obs_datetime}/{qc_status}/{acquisition_type}", response_model=observationinitial_schema.ObservationInitialWithChildrenResponse)
def get_observation_initial_by_id(recorded_from: str, described_by: int, obs_datetime: str, qc_status: int, acquisition_type: int):
    try:
        return get_success_response(
            result=[observationinitial_service.get(db_session=db.session, recorded_from=recorded_from, described_by=described_by, obs_datetime=obs_datetime, qc_status=qc_status, acquisition_type=acquisition_type)],
            message="Successfully fetched observation_initial."
        )
    except observationinitial_service.FailedGettingObservationInitial as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/observation-initial", response_model=observationinitial_schema.ObservationInitialResponse)
def create_observation_initial(data: observationinitial_schema.CreateObservationInitial):
    try:
        return get_success_response(
            result=[observationinitial_service.create(db_session=db.session, data=data)],
            message="Successfully created observation_initial."
        )
    except observationinitial_service.FailedCreatingObservationInitial as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/observation-initial/{recorded_from}/{described_by}/{obs_datetime}/{qc_status}/{acquisition_type}", response_model=observationinitial_schema.ObservationInitialResponse)
def update_observation_initial(recorded_from: str, described_by: int, obs_datetime: str, qc_status: int, acquisition_type: int, data: observationinitial_schema.UpdateObservationInitial):
    try:
        return get_success_response(
            result=[observationinitial_service.update(db_session=db.session, recorded_from=recorded_from, described_by=described_by, obs_datetime=obs_datetime, qc_status=qc_status, acquisition_type=acquisition_type, updates=data)],
            message="Successfully updated observation_initial."
        )
    except observationinitial_service.FailedUpdatingObservationInitial as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/observation-initial/{recorded_from}/{described_by}/{obs_datetime}/{qc_status}/{acquisition_type}", response_model=observationinitial_schema.ObservationInitialResponse)
def delete_observation_initial(recorded_from: str, described_by: int, obs_datetime: str, qc_status: int, acquisition_type: int):
    try:
        observationinitial_service.delete(db_session=db.session, recorded_from=recorded_from, described_by=described_by, obs_datetime=obs_datetime, qc_status=qc_status, acquisition_type=acquisition_type)
        return get_success_response(
            result=[],
            message="Successfully deleted observation_initial."
        )
    except observationinitial_service.FailedDeletingObservationInitial as e:
        return get_error_response(
            message=str(e)
        )






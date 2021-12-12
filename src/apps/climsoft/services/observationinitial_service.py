import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from apps.climsoft.schemas import observationinitial_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftObservationInitialService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingObservationInitial(Exception):
    pass


class FailedGettingObservationInitial(Exception):
    pass


class FailedGettingObservationInitialList(Exception):
    pass


class FailedUpdatingObservationInitial(Exception):
    pass


class FailedDeletingObservationInitial(Exception):
    pass


class ObservationInitialDoesNotExist(Exception):
    pass


def create(db_session: Session, data: observationinitial_schema.CreateObservationInitial) -> observationinitial_schema.ObservationInitial:
    try:
        observation_initial = models.Observationinitial(**data.dict())
        db_session.add(observation_initial)
        db_session.commit()
        print(observation_initial.obsDatetime)
        return observationinitial_schema.ObservationInitial.from_orm(observation_initial)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingObservationInitial("Failed creating observation_initial.")


def get(db_session: Session, recorded_from: str, described_by: int, obs_datetime: str, qc_status: int, acquisition_type: int) -> observationinitial_schema.ObservationInitialWithChildren:
    try:
        observation_initial = db_session.query(models.Observationinitial)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(obsDatetime=obs_datetime)\
            .filter_by(qcStatus=qc_status)\
            .filter_by(acquisitionType=acquisition_type)\
            .options(joinedload("obselement"), joinedload("station"))\
            .first()

        if not observation_initial:
            raise HTTPException(status_code=404, detail="ObservationInitial does not exist.")

        return observationinitial_schema.ObservationInitialWithChildren.from_orm(observation_initial)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingObservationInitial("Failed getting observation_initial.")


def query(
        db_session: Session,
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
        cloud_height_units: str = None,
        vis_units: str = None,
        data_source_timezone: int = None,
        limit: int = 25,
        offset: int = 0
) -> List[observationinitial_schema.ObservationInitial]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `observationinitial` row skipping
    `offset` number of rows
    :param db_session: db session
    :param recorded_from:
    :param described_by:
    :param obs_datetime:
    :param qc_status:
    :param acquisition_type:
    :param obs_level:
    :param obs_value:
    :param flag:
    :param period:
    :param qc_type_log:
    :param data_form:
    :param captured_by:
    :param mark:
    :param temperature_units:
    :param precipitation_units:
    :param cloud_height_units:
    :param vis_units:
    :param data_source_timezone:
    :param limit:
    :param offset:
    :return:
    """
    try:
        q = db_session.query(models.Observationinitial)

        if recorded_from is not None:
            q = q.filter_by(recordedFrom=recorded_from)

        if described_by is not None:
            q = q.filter_by(describedBy=described_by)

        if obs_datetime is not None:
            q = q.filter_by(obsDatetime=obs_datetime)

        if qc_status is not None:
            q = q.filter_by(qcStatus=qc_status)

        if acquisition_type is not None:
            q = q.filter_by(acquisitionType=acquisition_type)

        if obs_level is not None:
            q = q.filter_by(obsLevel=obs_level)

        if obs_value is not None:
            q = q.filter_by(obsValue=obs_value)

        if flag is not None:
            q = q.filter_by(flag=flag)

        if period is not None:
            q = q.filter(models.Observationinitial.period >= period)

        if qc_type_log is not None:
            q = q.filter(models.Observationinitial.qcTypeLog.ilike(f"%{qc_type_log}%"))

        if data_form is not None:
            q = q.filter(models.Observationinitial.dataForm.ilike(f"%{data_form}%"))

        if captured_by is not None:
            q = q.filter_by(capturedBy=captured_by)

        if mark is not None:
            q = q.filter_by(mark=mark)

        if temperature_units is not None:
            q = q.filter(models.Observationinitial.temperatureUnits.ilike(f"%{temperature_units}%"))

        if precipitation_units is not None:
            q = q.filter(models.Observationinitial.precipitationUnits.ilike(f"%{precipitation_units}%"))

        if cloud_height_units is not None:
            q = q.filter(models.Observationinitial.cloudHeightUnits.ilike(f"%{cloud_height_units}%"))

        if vis_units is not None:
            q = q.filter_by(models.Observationinitial.visUnits.ilike(f"%{vis_units}%"))

        if data_source_timezone is not None:
            q = q.filter_by(dataSourceTimezone=data_source_timezone)

        return [observationinitial_schema.ObservationInitial.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingObservationInitialList("Failed getting observation_initial list.")


def update(db_session: Session, recorded_from: str, described_by: int, obs_datetime: str, qc_status: int, acquisition_type: int, updates: observationinitial_schema.UpdateObservationInitial) -> observationinitial_schema.ObservationInitial:
    try:
        db_session.query(models.Observationinitial)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(obsDatetime=obs_datetime)\
            .filter_by(qcStatus=qc_status)\
            .filter_by(acquisitionType=acquisition_type)\
            .update(updates.dict())
        db_session.commit()
        updated_instrument = db_session.query(models.Observationinitial)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(obsDatetime=obs_datetime)\
            .filter_by(qcStatus=qc_status)\
            .filter_by(acquisitionType=acquisition_type)\
            .first()
        return observationinitial_schema.ObservationInitial.from_orm(updated_instrument)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingObservationInitial("Failed updating observation_initial")


def delete(db_session: Session, recorded_from: str, described_by: int, obs_datetime: str, qc_status: int, acquisition_type: int) -> bool:
    try:
        db_session.query(models.Observationinitial)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(obsDatetime=obs_datetime)\
            .filter_by(qcStatus=qc_status)\
            .filter_by(acquisitionType=acquisition_type)\
            .delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingObservationInitial("Failed deleting observation_initial.")





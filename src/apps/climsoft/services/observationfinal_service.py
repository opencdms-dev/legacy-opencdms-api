import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import observationfinal_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftObservationFinalService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingObservationFinal(Exception):
    pass


class FailedGettingObservationFinal(Exception):
    pass


class FailedGettingObservationFinalList(Exception):
    pass


class FailedUpdatingObservationFinal(Exception):
    pass


class FailedDeletingObservationFinal(Exception):
    pass


class ObservationFinalDoesNotExist(Exception):
    pass


def create(db_session: Session, data: observationfinal_schema.CreateObservationFinal) -> observationfinal_schema.ObservationFinal:
    try:
        observation_final = models.Observationfinal(**data.dict())
        db_session.add(observation_final)
        db_session.commit()
        print(observation_final.obsDatetime)
        return observationfinal_schema.ObservationFinal.from_orm(observation_final)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingObservationFinal("Failed creating observation_final.")


def get(db_session: Session, recorded_from: str, described_by: int, obs_datetime: str) -> observationfinal_schema.ObservationFinalWithChildren:
    try:
        observation_final = db_session.query(models.Observationfinal)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(obsDatetime=obs_datetime)\
            .options(joinedload("obselement"), joinedload("station"))\
            .first()

        if not observation_final:
            raise HTTPException(status_code=404, detail="ObservationFinal does not exist.")

        return observationfinal_schema.ObservationFinalWithChildren.from_orm(observation_final)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingObservationFinal("Failed getting observation_final.")


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
) -> List[observationfinal_schema.ObservationFinal]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `observationfinal` row skipping
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
        q = db_session.query(models.Observationfinal)

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
            q = q.filter(models.Observationfinal.period >= period)

        if qc_type_log is not None:
            q = q.filter(models.Observationfinal.qcTypeLog.ilike(f"%{qc_type_log}%"))

        if data_form is not None:
            q = q.filter(models.Observationfinal.dataForm.ilike(f"%{data_form}%"))

        if captured_by is not None:
            q = q.filter_by(capturedBy=captured_by)

        if mark is not None:
            q = q.filter_by(mark=mark)

        if temperature_units is not None:
            q = q.filter(models.Observationfinal.temperatureUnits.ilike(f"%{temperature_units}%"))

        if precipitation_units is not None:
            q = q.filter(models.Observationfinal.precipitationUnits.ilike(f"%{precipitation_units}%"))

        if cloud_height_units is not None:
            q = q.filter(models.Observationfinal.cloudHeightUnits.ilike(f"%{cloud_height_units}%"))

        if vis_units is not None:
            q = q.filter_by(models.Observationfinal.visUnits.ilike(f"%{vis_units}%"))

        if data_source_timezone is not None:
            q = q.filter_by(dataSourceTimezone=data_source_timezone)

        return [observationfinal_schema.ObservationFinal.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingObservationFinalList("Failed getting observation_final list.")


def update(db_session: Session, recorded_from: str, described_by: int, obs_datetime: str, updates: observationfinal_schema.UpdateObservationFinal) -> observationfinal_schema.ObservationFinal:
    try:
        db_session.query(models.Observationfinal)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(obsDatetime=obs_datetime)\
            .update(updates.dict())
        db_session.commit()
        updated_instrument = db_session.query(models.Observationfinal)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(obsDatetime=obs_datetime)\
            .first()
        return observationfinal_schema.ObservationFinal.from_orm(updated_instrument)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingObservationFinal("Failed updating observation_final")


def delete(db_session: Session, recorded_from: str, described_by: int, obs_datetime: str) -> bool:
    try:
        db_session.query(models.Observationfinal)\
            .filter_by(recordedFrom=recorded_from)\
            .filter_by(describedBy=described_by)\
            .filter_by(obsDatetime=obs_datetime)\
            .delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingObservationFinal("Failed deleting observation_final.")





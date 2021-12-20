import logging
from typing import List
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from opencdms.models.climsoft import v4_1_1_core as models
from apps.climsoft.schemas import instrument_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftInstrumentService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingInstrument(Exception):
    pass


class FailedGettingInstrument(Exception):
    pass


class FailedGettingInstrumentList(Exception):
    pass


class FailedUpdatingInstrument(Exception):
    pass


class FailedDeletingInstrument(Exception):
    pass


class InstrumentDoesNotExist(Exception):
    pass


def create(db_session: Session, data: instrument_schema.CreateInstrument) -> instrument_schema.Instrument:
    try:
        instrument = models.Instrument(**data.dict())
        db_session.add(instrument)
        db_session.commit()
        return instrument_schema.Instrument.from_orm(instrument)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingInstrument("Failed creating instrument.")


def get(db_session: Session, instrument_id: str) -> instrument_schema.Instrument:
    try:
        instrument = db_session.query(models.Instrument).filter_by(instrumentId=instrument_id).options(joinedload('station')).first()

        if not instrument:
            raise HTTPException(status_code=404, detail="Instrument does not exist.")

        return instrument_schema.InstrumentWithStation.from_orm(instrument)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingInstrument("Failed getting instrument.")


def query(
        db_session: Session,
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
        offset: int = 0
) -> List[instrument_schema.Instrument]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `instrument` row skipping
    `offset` number of rows

    :param db_session: database session
    :param instrument_id: compares with `instrumentId` column for exact match
    :param instrument_name: compares with `instrumentName` column for exact match
    :param serial_number: compares with `serialNumber` column for exact match
    :param abbreviation: compares with `abbreviation` column for exact match
    :param model: checks if the model column contains given input
    :param manufacturer: checks if the manufacturer column contains given input
    :param instrument_uncertainty: returns items with lower or equal instrumentUncertainty
    :param installation_datetime: returns items with installationDatetime greater that given input
    :param uninstallation_datetime: returns items with deinstallationDatetime smaller that given input
    :param height: returns items with height greater that given input
    :param station_id: compares with installedAt column for exact match
    :param limit: takes first `limit` number of rows
    :param offset: skips first `offset` number of rows
    :return: list of `instrument`
    """
    try:
        q = db_session.query(models.Instrument)

        if instrument_id is not None:
            q = q.filter_by(instrumentId=instrument_id)

        if instrument_name is not None:
            q = q.filter_by(instrumentName=instrument_name)

        if serial_number is not None:
            q = q.filter_by(serialNumber=serial_number)

        if abbreviation is not None:
            q = q.filter_by(abbreviation=abbreviation)

        if model is not None:
            q = q.filter(models.Instrument.model.ilike(f"%{model}%"))

        if manufacturer is not None:
            q = q.filter(models.Instrument.manufacturer.ilike(f"%{manufacturer}%"))

        if instrument_uncertainty is not None:
            q = q.filter(models.Instrument.instrumentUncertainty <= instrument_uncertainty)

        if installation_datetime is not None:
            q = q.filter(models.Instrument.installationDatetime >= installation_datetime)

        if uninstallation_datetime is not None:
            q = q.filter(models.Instrument.deinstallationDatetime <= uninstallation_datetime)

        if height is not None:
            q = q.filter(models.Instrument.height > height)

        if station_id is not None:
            q = q.filter_by(installedAt=station_id)

        return [instrument_schema.Instrument.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingInstrumentList("Failed getting instrument list.")


def update(db_session: Session, instrument_id: str, updates: instrument_schema.UpdateInstrument) -> instrument_schema.Instrument:
    try:
        db_session.query(models.Instrument).filter_by(instrumentId=instrument_id).update(updates.dict())
        db_session.commit()
        updated_instrument = db_session.query(models.Instrument).filter_by(instrumentId=instrument_id).first()
        return instrument_schema.Instrument.from_orm(updated_instrument)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingInstrument("Failed updating instrument")


def delete(db_session: Session, instrument_id: str) -> bool:
    try:
        db_session.query(models.Instrument).filter_by(instrumentId=instrument_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingInstrument("Failed deleting instrument.")





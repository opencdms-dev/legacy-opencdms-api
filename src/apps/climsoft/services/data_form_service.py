import logging
from typing import List
from sqlalchemy.orm.session import Session
from opencdms.models.climsoft import v4_1_1_core as models
from src.apps.climsoft.schemas import data_form_schema
from fastapi.exceptions import HTTPException

logger = logging.getLogger("ClimsoftDataFormService")
logging.basicConfig(level=logging.INFO)


class FailedCreatingDataForm(Exception):
    pass


class FailedGettingDataForm(Exception):
    pass


class FailedGettingDataFormList(Exception):
    pass


class FailedUpdatingDataForm(Exception):
    pass


class FailedDeletingDataForm(Exception):
    pass


class DataFormDoesNotExist(Exception):
    pass


def create(db_session: Session, data: data_form_schema.CreateDataForm) -> data_form_schema.DataForm:
    try:
        data_form = models.DataForm(**data.dict())
        db_session.add(data_form)
        db_session.commit()
        return data_form_schema.DataForm.from_orm(data_form)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedCreatingDataForm("Failed creating data_form.")


def get(db_session: Session, data_form_id: str) -> data_form_schema.DataForm:
    try:
        data_form = db_session.query(models.DataForm).filter_by(data_formId=data_form_id).first()

        if not data_form:
            raise HTTPException(status_code=404, detail="DataForm does not exist.")

        return data_form_schema.DataForm.from_orm(data_form)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(e)
        raise FailedGettingDataForm("Failed getting data_form.")


def query(
        db_session: Session,
        order_num: int = None,
        table_name: str = None,
        form_name: str = None,
        description: str = None,
        selected: bool = None,
        val_start_position: int = None,
        val_end_position: int = None,
        elem_code_location: str = None,
        sequencer: str = None,
        entry_mode: bool = None,
        limit: int = 25,
        offset: int = 0
) -> List[data_form_schema.DataForm]:
    """
    This function builds a query based on the given parameter and returns `limit` numbers of `data_forms` row skipping
    `offset` number of rows

    """
    try:
        q = db_session.query(models.DataForm)

        if order_num is not None:
            q = q.filter_by(order_num=order_num)

        if table_name is not None:
            q = q.filter_by(table_name=table_name)

        if form_name is not None:
            q = q.filter_by(form_name=form_name)

        if description is not None:
            q = q.filter(models.DataForm.description.ilike(f"%{description}%"))

        if selected is not None:
            q = q.filter_by(selected=selected)

        if val_start_position is not None:
            q = q.filter_by(val_start_position=val_start_position)

        if val_end_position is not None:
            q = q.filter_by(val_end_position=val_end_position)

        if elem_code_location is not None:
            q = q.filter_by(elem_code_location=elem_code_location)

        if sequencer is not None:
            q = q.filter_by(sequencer=sequencer)

        if entry_mode is not None:
            q = q.filter(models.DataForm.entry_mode.ilike(f"%{entry_mode}%"))

        return [data_form_schema.DataForm.from_orm(s) for s in q.offset(offset).limit(limit).all()]
    except Exception as e:
        logger.exception(e)
        raise FailedGettingDataFormList("Failed getting data form list.")


def update(db_session: Session, form_name: str, updates: data_form_schema.UpdateDataForm) -> data_form_schema.DataForm:
    try:
        db_session.query(models.DataForm).filter_by(form_name=form_name).update(updates.dict())
        db_session.commit()
        updated_data_form = db_session.query(models.DataForm).filter_by(form_name=form_name).first()
        return data_form_schema.DataForm.from_orm(updated_data_form)
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedUpdatingDataForm("Failed updating data form")


def delete(db_session: Session, form_name: str) -> bool:
    try:
        db_session.query(models.DataForm).filter_by(form_name=form_name).delete()
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        logger.exception(e)
        raise FailedDeletingDataForm("Failed deleting data form.")





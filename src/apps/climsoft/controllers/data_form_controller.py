from fastapi import APIRouter, Depends
from apps.climsoft.services import data_form_service
from apps.climsoft.schemas import data_form_schema
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


@router.get("/data-forms", response_model=data_form_schema.DataFormResponse)
def get_data_forms(
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
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        data_forms = data_form_service.query(
            db_session=db_session,
            order_num=order_num,
            table_name=table_name,
            form_name=form_name,
            description=description,
            selected=selected,
            val_start_position=val_start_position,
            val_end_position=val_end_position,
            elem_code_location=elem_code_location,
            sequencer=sequencer,
            entry_mode=entry_mode,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=data_forms, message="Successfully fetched data_forms.")
    except data_form_service.FailedGettingDataFormList as e:
        return get_error_response(message=str(e))


@router.get("/data-forms/{form_name}", response_model=data_form_schema.DataFormResponse)
def get_data_form_by_id(form_name: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[data_form_service.get(db_session=db_session, form_name=form_name)],
            message="Successfully fetched data_form."
        )
    except data_form_service.FailedGettingDataForm as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/data-forms", response_model=data_form_schema.DataFormResponse)
def create_data_form(data: data_form_schema.CreateDataForm, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[data_form_service.create(db_session=db_session, data=data)],
            message="Successfully created data_form."
        )
    except data_form_service.FailedCreatingDataForm as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/data-forms/{form_name}", response_model=data_form_schema.DataFormResponse)
def update_data_form(form_name: str, data: data_form_schema.UpdateDataForm, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[data_form_service.update(db_session=db_session, form_name=form_name, updates=data)],
            message="Successfully updated data_form."
        )
    except data_form_service.FailedUpdatingDataForm as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/data-forms/{form_name}", response_model=data_form_schema.DataFormResponse)
def delete_data_form(form_name: str, db_session: Session = Depends(get_db)):
    try:
        data_form_service.delete(db_session=db_session, form_name=form_name)
        return get_success_response(
            result=[],
            message="Successfully deleted data_form."
        )
    except data_form_service.FailedDeletingDataForm as e:
        return get_error_response(
            message=str(e)
        )






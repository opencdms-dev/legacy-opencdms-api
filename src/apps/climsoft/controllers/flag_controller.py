from fastapi import APIRouter, Depends
from src.apps.climsoft.services import flag_service
from src.apps.climsoft.schemas import flag_schema
from src.utils.response import get_success_response, get_error_response
from sqlalchemy.orm.session import Session
from src.apps.climsoft.db.engine import SessionLocal
from src.dependencies import auth


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


@router.get("/data-forms", response_model=flag_schema.FlagResponse)
def get_flags(
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
        flags = flag_service.query(
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

        return get_success_response(result=flags, message="Successfully fetched flags.")
    except flag_service.FailedGettingFlagList as e:
        return get_error_response(message=str(e))


@router.get("/data-forms/{form_name}", response_model=flag_schema.FlagResponse)
def get_flag_by_id(form_name: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[flag_service.get(db_session=db_session, form_name=form_name)],
            message="Successfully fetched flag."
        )
    except flag_service.FailedGettingFlag as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/data-forms", response_model=flag_schema.FlagResponse)
def create_flag(data: flag_schema.CreateFlag, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[flag_service.create(db_session=db_session, data=data)],
            message="Successfully created flag."
        )
    except flag_service.FailedCreatingFlag as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/data-forms/{form_name}", response_model=flag_schema.FlagResponse)
def update_flag(form_name: str, data: flag_schema.UpdateFlag, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[flag_service.update(db_session=db_session, form_name=form_name, updates=data)],
            message="Successfully updated flag."
        )
    except flag_service.FailedUpdatingFlag as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/data-forms/{form_name}", response_model=flag_schema.FlagResponse)
def delete_flag(form_name: str, db_session: Session = Depends(get_db)):
    try:
        flag_service.delete(db_session=db_session, form_name=form_name)
        return get_success_response(
            result=[],
            message="Successfully deleted flag."
        )
    except flag_service.FailedDeletingFlag as e:
        return get_error_response(
            message=str(e)
        )






from fastapi import APIRouter, Depends
from apps.climsoft.services import flag_service
from apps.climsoft.schemas import flag_schema
from utils.response import get_success_response, get_error_response
from sqlalchemy.orm.session import Session
from apps.climsoft.db.engine import SessionLocal
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


@router.get("/flags", response_model=flag_schema.FlagResponse)
def get_flags(
        character_symbol: str = None,
        num_symbol: int = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        flags = flag_service.query(
            db_session=db_session,
            character_symbol=character_symbol,
            num_symbol=num_symbol,
            description=description,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=flags, message="Successfully fetched flags.")
    except flag_service.FailedGettingFlagList as e:
        return get_error_response(message=str(e))


@router.get("/flags/{character_symbol}", response_model=flag_schema.FlagResponse)
def get_flag_by_id(character_symbol: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[flag_service.get(db_session=db_session, character_symbol=character_symbol)],
            message="Successfully fetched flag."
        )
    except flag_service.FailedGettingFlag as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/flags", response_model=flag_schema.FlagResponse)
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


@router.put("/flags/{character_symbol}", response_model=flag_schema.FlagResponse)
def update_flag(character_symbol: str, data: flag_schema.UpdateFlag, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[flag_service.update(db_session=db_session, character_symbol=character_symbol, updates=data)],
            message="Successfully updated flag."
        )
    except flag_service.FailedUpdatingFlag as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/flags/{character_symbol}", response_model=flag_schema.FlagResponse)
def delete_flag(character_symbol: str, db_session: Session = Depends(get_db)):
    try:
        flag_service.delete(db_session=db_session, character_symbol=character_symbol)
        return get_success_response(
            result=[],
            message="Successfully deleted flag."
        )
    except flag_service.FailedDeletingFlag as e:
        return get_error_response(
            message=str(e)
        )






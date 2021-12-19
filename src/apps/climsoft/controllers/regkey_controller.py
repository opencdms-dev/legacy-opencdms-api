from fastapi import APIRouter, Depends
from apps.climsoft.services import regkey_service
from apps.climsoft.schemas import regkey_schema
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


@router.get("/reg-keys", response_model=regkey_schema.RegKeyResponse)
def get_reg_keys(
        key_name: str = None,
        key_value: str = None,
        key_description: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        reg_keys = regkey_service.query(
            db_session=db_session,
            key_name=key_name,
            key_value=key_value,
            key_description=key_description,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=reg_keys, message="Successfully fetched reg_keys.")
    except regkey_service.FailedGettingRegKeyList as e:
        return get_error_response(message=str(e))


@router.get("/reg-keys/{key_name}", response_model=regkey_schema.RegKeyResponse)
def get_reg_key_by_id(key_name: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[regkey_service.get(db_session=db_session, key_name=key_name)],
            message="Successfully fetched reg_key."
        )
    except regkey_service.FailedGettingRegKey as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/reg-keys", response_model=regkey_schema.RegKeyResponse)
def create_reg_key(data: regkey_schema.CreateRegKey, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[regkey_service.create(db_session=db_session, data=data)],
            message="Successfully created reg_key."
        )
    except regkey_service.FailedCreatingRegKey as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/reg-keys/{key_name}", response_model=regkey_schema.RegKeyResponse)
def update_reg_key(key_name: str, data: regkey_schema.UpdateRegKey, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[regkey_service.update(db_session=db_session, key_name=key_name, updates=data)],
            message="Successfully updated reg_key."
        )
    except regkey_service.FailedUpdatingRegKey as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/reg-keys/{key_name}", response_model=regkey_schema.RegKeyResponse)
def delete_reg_key(key_name: str, db_session: Session = Depends(get_db)):
    try:
        regkey_service.delete(db_session=db_session, key_name=key_name)
        return get_success_response(
            result=[],
            message="Successfully deleted reg_key."
        )
    except regkey_service.FailedDeletingRegKey as e:
        return get_error_response(
            message=str(e)
        )






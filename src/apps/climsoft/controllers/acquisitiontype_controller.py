from fastapi import APIRouter, Depends
from src.apps.climsoft.services import acquisitiontype_service
from src.apps.climsoft.schemas import acquisitiontype_schema
from src.utils.response import get_success_response, get_error_response
from sqlalchemy.orm.session import Session
from src.apps.climsoft.db.engine import SessionLocal


router = APIRouter(
    prefix="/api/v1/climsoft",
    tags=["climsoft"]
)


async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/acquisition-types", response_model=acquisitiontype_schema.AcquisitionTypeResponse)
def get_acquisition_types(
        code: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        stations = acquisitiontype_service.query(
            db_session=db_session,
            code=code,
            description=description,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=stations, message="Successfully fetched stations.")
    except acquisitiontype_service.FailedGettingAcquisitionTypeList as e:
        return get_error_response(message=str(e))


@router.get("/acquisition-types/{code}", response_model=acquisitiontype_schema.AcquisitionTypeResponse)
def get_acquisition_type_by_id(code: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[acquisitiontype_service.get(db_session=db_session, code=code)],
            message="Successfully fetched station."
        )
    except acquisitiontype_service.FailedGettingAcquisitionType as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/acquisition-types", response_model=acquisitiontype_schema.AcquisitionTypeResponse)
def create_acquisition_type(data: acquisitiontype_schema.CreateAcquisitionType, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[acquisitiontype_service.create(db_session=db_session, data=data)],
            message="Successfully created station."
        )
    except acquisitiontype_service.FailedCreatingAcquisitionType as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/acquisition-types/{code}", response_model=acquisitiontype_schema.AcquisitionTypeResponse)
def update_acquisition_type(code: str, data: acquisitiontype_schema.UpdateAcquisitionType, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[acquisitiontype_service.update(db_session=db_session, code=code, updates=data)],
            message="Successfully updated station."
        )
    except acquisitiontype_service.FailedUpdatingAcquisitionType as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/acquisition-types/{code}", response_model=acquisitiontype_schema.AcquisitionTypeResponse)
def delete_acquisition_type(code: str, db_session: Session = Depends(get_db)):
    try:
        acquisitiontype_service.delete(db_session=db_session, code=code)
        return get_success_response(
            result=[],
            message="Successfully deleted station."
        )
    except acquisitiontype_service.FailedDeletingAcquisitionType as e:
        return get_error_response(
            message=str(e)
        )






from fastapi import APIRouter, Depends
from apps.climsoft.services import synopfeature_service
from apps.climsoft.schemas import synopfeature_schema
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


@router.get("/synop-features", response_model=synopfeature_schema.SynopFeatureResponse)
def get_qc_types(
        abbreviation: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        qc_types = synopfeature_service.query(
            db_session=db_session,
            abbreviation=abbreviation,
            description=description,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=qc_types, message="Successfully fetched qc_types.")
    except synopfeature_service.FailedGettingSynopFeatureList as e:
        return get_error_response(message=str(e))


@router.get("/synop-features/{abbreviation}", response_model=synopfeature_schema.SynopFeatureResponse)
def get_qc_type_by_id(abbreviation: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[synopfeature_service.get(db_session=db_session, abbreviation=abbreviation)],
            message="Successfully fetched qc_type."
        )
    except synopfeature_service.FailedGettingSynopFeature as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/synop-features", response_model=synopfeature_schema.SynopFeatureResponse)
def create_qc_type(data: synopfeature_schema.CreateSynopFeature, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[synopfeature_service.create(db_session=db_session, data=data)],
            message="Successfully created qc_type."
        )
    except synopfeature_service.FailedCreatingSynopFeature as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/synop-features/{abbreviation}", response_model=synopfeature_schema.SynopFeatureResponse)
def update_qc_type(abbreviation: str, data: synopfeature_schema.UpdateSynopFeature, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[synopfeature_service.update(db_session=db_session, abbreviation=abbreviation, updates=data)],
            message="Successfully updated qc_type."
        )
    except synopfeature_service.FailedUpdatingSynopFeature as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/synop-features/{abbreviation}", response_model=synopfeature_schema.SynopFeatureResponse)
def delete_qc_type(abbreviation: str, db_session: Session = Depends(get_db)):
    try:
        synopfeature_service.delete(db_session=db_session, abbreviation=abbreviation)
        return get_success_response(
            result=[],
            message="Successfully deleted qc_type."
        )
    except synopfeature_service.FailedDeletingSynopFeature as e:
        return get_error_response(
            message=str(e)
        )






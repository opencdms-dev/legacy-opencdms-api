from fastapi import APIRouter, Depends
from apps.climsoft.services import physicalfeature_service
from apps.climsoft.schemas import physicalfeature_schema
from utils.response import get_success_response, get_error_response
from apps.climsoft.db.engine import SessionLocal
from sqlalchemy.orm.session import Session
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


@router.get("/physical-features", response_model=physicalfeature_schema.PhysicalFeatureResponse)
def get_physical_feature(
    associated_with: str = None,
    begin_date: str = None,
    end_date: str = None,
    image: str = None,
    description: str = None,
    classified_into: str = None,
    limit: int = 25,
    offset: int = 0,
    db_session: Session = Depends(get_db)
):
    try:
        physical_feature = physicalfeature_service.query(
            db_session=db_session,
            associated_with=associated_with,
            begin_date=begin_date,
            end_date=end_date,
            image=image,
            description=description,
            classified_into=classified_into,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=physical_feature, message="Successfully fetched physical_feature.")
    except physicalfeature_service.FailedGettingPhysicalFeatureList as e:
        return get_error_response(message=str(e))


@router.get("/physical-features/{associated_with}/{begin_date}/{classified_into}/{description}", response_model=physicalfeature_schema.PhysicalFeatureWithStationAndPhysicalFeatureClassResponse)
def get_physical_feature_by_id(associated_with: str, begin_date: str, classified_into: str, description: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[physicalfeature_service.get(db_session=db_session, associated_with=associated_with, begin_date=begin_date, classified_into=classified_into, description=description)],
            message="Successfully fetched physical_feature."
        )
    except physicalfeature_service.FailedGettingPhysicalFeature as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/physical-features", response_model=physicalfeature_schema.PhysicalFeatureResponse)
def create_physical_feature(data: physicalfeature_schema.CreatePhysicalFeature, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[physicalfeature_service.create(db_session=db_session, data=data)],
            message="Successfully created physical_feature."
        )
    except physicalfeature_service.FailedCreatingPhysicalFeature as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/physical-features/{associated_with}/{begin_date}/{classified_into}/{description}", response_model=physicalfeature_schema.PhysicalFeatureResponse)
def update_physical_feature(associated_with: str, begin_date: str, classified_into: str, description: str, data: physicalfeature_schema.UpdatePhysicalFeature, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[physicalfeature_service.update(db_session=db_session, associated_with=associated_with, begin_date=begin_date, classified_into=classified_into, description=description, updates=data)],
            message="Successfully updated physical_feature."
        )
    except physicalfeature_service.FailedUpdatingPhysicalFeature as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/physical-features/{associated_with}/{begin_date}/{classified_into}/{description}", response_model=physicalfeature_schema.PhysicalFeatureResponse)
def delete_physical_feature(associated_with: str, begin_date: str, classified_into: str, description: str, db_session: Session = Depends(get_db)):
    try:
        physicalfeature_service.delete(db_session=db_session, associated_with=associated_with, begin_date=begin_date, classified_into=classified_into, description=description)
        return get_success_response(
            result=[],
            message="Successfully deleted physical_feature."
        )
    except physicalfeature_service.FailedDeletingPhysicalFeature as e:
        return get_error_response(
            message=str(e)
        )






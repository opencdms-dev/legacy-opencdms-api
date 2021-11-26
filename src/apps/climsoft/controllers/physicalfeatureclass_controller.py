from fastapi import APIRouter, Depends
from src.apps.climsoft.services import physicalfeatureclass_service
from src.apps.climsoft.schemas import physicalfeatureclass_schema
from src.utils.response import get_success_response, get_error_response
from src.apps.climsoft.db.engine import SessionLocal
from sqlalchemy.orm.session import Session
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


@router.get("/physical-feature-class", response_model=physicalfeatureclass_schema.PhysicalFeatureClassResponse)
def get_physical_feature_class(
        feature_class: str = None,
        description: str = None,
        refers_to: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        physical_feature_class = physicalfeatureclass_service.query(
            db_session=db_session,
            feature_class=feature_class,
            description=description,
            refers_to=refers_to,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=physical_feature_class, message="Successfully fetched physical_feature_class.")
    except physicalfeatureclass_service.FailedGettingPhysicalFeatureClassList as e:
        return get_error_response(message=str(e))


@router.get("/physical-feature-class/{feature_class}", response_model=physicalfeatureclass_schema.PhysicalFeatureClassWithStationResponse)
def get_physical_feature_class_by_id(feature_class: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[physicalfeatureclass_service.get(db_session=db_session, feature_class=feature_class)],
            message="Successfully fetched physical_feature_class."
        )
    except physicalfeatureclass_service.FailedGettingPhysicalFeatureClass as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/physical-feature-class", response_model=physicalfeatureclass_schema.PhysicalFeatureClassResponse)
def create_physical_feature_class(data: physicalfeatureclass_schema.CreatePhysicalFeatureClass, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[physicalfeatureclass_service.create(db_session=db_session, data=data)],
            message="Successfully created physical_feature_class."
        )
    except physicalfeatureclass_service.FailedCreatingPhysicalFeatureClass as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/physical-feature-class/{feature_class}", response_model=physicalfeatureclass_schema.PhysicalFeatureClassResponse)
def update_physical_feature_class(feature_class: str, data: physicalfeatureclass_schema.UpdatePhysicalFeatureClass, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[physicalfeatureclass_service.update(db_session=db_session, feature_class=feature_class, updates=data)],
            message="Successfully updated physical_feature_class."
        )
    except physicalfeatureclass_service.FailedUpdatingPhysicalFeatureClass as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/physical-feature-class/{feature_class}", response_model=physicalfeatureclass_schema.PhysicalFeatureClassResponse)
def delete_physical_feature_class(feature_class: str, db_session: Session = Depends(get_db)):
    try:
        physicalfeatureclass_service.delete(db_session=db_session, feature_class=feature_class)
        return get_success_response(
            result=[],
            message="Successfully deleted physical_feature_class."
        )
    except physicalfeatureclass_service.FailedDeletingPhysicalFeatureClass as e:
        return get_error_response(
            message=str(e)
        )






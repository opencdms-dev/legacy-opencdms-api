from fastapi import APIRouter, Depends
from apps.climsoft.services import obselement_service
from apps.climsoft.schemas import obselement_schema
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


@router.get("/obselements", response_model=obselement_schema.ObsElementResponse)
def get_obselements(
        element_id: str = None,
        element_name: str = None,
        abbreviation: str = None,
        description: str = None,
        element_scale: float = None,
        upper_limit: float = None,
        lower_limit: str = None,
        units: str = None,
        element_type: str = None,
        qc_total_required: int = None,
        selected: bool = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        obselements = obselement_service.query(
            db_session=db_session,
            element_id=element_id,
            element_name=element_name,
            abbreviation=abbreviation,
            description=description,
            element_scale=element_scale,
            upper_limit=upper_limit,
            lower_limit=lower_limit,
            units=units,
            element_type=element_type,
            qc_total_required=qc_total_required,
            selected=selected,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=obselements, message="Successfully fetched obselements.")
    except obselement_service.FailedGettingObsElementList as e:
        return get_error_response(message=str(e))


@router.get("/obselements/{element_id}", response_model=obselement_schema.ObsElementResponse)
def get_obs_element_by_id(element_id: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[obselement_service.get(db_session=db_session, element_id=element_id)],
            message="Successfully fetched obs_element."
        )
    except obselement_service.FailedGettingObsElement as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/obselements", response_model=obselement_schema.ObsElementResponse)
def create_obs_element(data: obselement_schema.CreateObsElement, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[obselement_service.create(db_session=db_session, data=data)],
            message="Successfully created obs_element."
        )
    except obselement_service.FailedCreatingObsElement as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/obselements/{element_id}", response_model=obselement_schema.ObsElementResponse)
def update_obs_element(element_id: str, data: obselement_schema.UpdateObsElement, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[obselement_service.update(db_session=db_session, element_id=element_id, updates=data)],
            message="Successfully updated obs_element."
        )
    except obselement_service.FailedUpdatingObsElement as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/obselements/{element_id}", response_model=obselement_schema.ObsElementResponse)
def delete_obs_element(element_id: str, db_session: Session = Depends(get_db)):
    try:
        obselement_service.delete(db_session=db_session, element_id=element_id)
        return get_success_response(
            result=[],
            message="Successfully deleted obs_element."
        )
    except obselement_service.FailedDeletingObsElement as e:
        return get_error_response(
            message=str(e)
        )






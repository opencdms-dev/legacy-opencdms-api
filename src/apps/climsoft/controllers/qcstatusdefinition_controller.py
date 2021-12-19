from fastapi import APIRouter, Depends
from apps.climsoft.services import qcstatusdefinition_service
from apps.climsoft.schemas import qcstatusdefinition_schema
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


@router.get("/qc-status-definitions", response_model=qcstatusdefinition_schema.QCStatusDefinitionResponse)
def get_qc_status_definitions(
        code: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        qc_status_definitions = qcstatusdefinition_service.query(
            db_session=db_session,
            code=code,
            description=description,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=qc_status_definitions, message="Successfully fetched qc_status_definitions.")
    except qcstatusdefinition_service.FailedGettingQCStatusDefinitionList as e:
        return get_error_response(message=str(e))


@router.get("/qc-status-definitions/{code}", response_model=qcstatusdefinition_schema.QCStatusDefinitionResponse)
def get_qc_status_definition_by_id(code: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[qcstatusdefinition_service.get(db_session=db_session, code=code)],
            message="Successfully fetched qc_status_definition."
        )
    except qcstatusdefinition_service.FailedGettingQCStatusDefinition as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/qc-status-definitions", response_model=qcstatusdefinition_schema.QCStatusDefinitionResponse)
def create_qc_status_definition(data: qcstatusdefinition_schema.CreateQCStatusDefinition, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[qcstatusdefinition_service.create(db_session=db_session, data=data)],
            message="Successfully created qc_status_definition."
        )
    except qcstatusdefinition_service.FailedCreatingQCStatusDefinition as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/qc-status-definitions/{code}", response_model=qcstatusdefinition_schema.QCStatusDefinitionResponse)
def update_qc_status_definition(code: str, data: qcstatusdefinition_schema.UpdateQCStatusDefinition, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[qcstatusdefinition_service.update(db_session=db_session, code=code, updates=data)],
            message="Successfully updated qc_status_definition."
        )
    except qcstatusdefinition_service.FailedUpdatingQCStatusDefinition as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/qc-status-definitions/{code}", response_model=qcstatusdefinition_schema.QCStatusDefinitionResponse)
def delete_qc_status_definition(code: str, db_session: Session = Depends(get_db)):
    try:
        qcstatusdefinition_service.delete(db_session=db_session, code=code)
        return get_success_response(
            result=[],
            message="Successfully deleted qc_status_definition."
        )
    except qcstatusdefinition_service.FailedDeletingQCStatusDefinition as e:
        return get_error_response(
            message=str(e)
        )






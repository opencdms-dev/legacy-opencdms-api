from fastapi import APIRouter, Depends
from src.apps.climsoft.services import paperarchivedefinition_service
from src.apps.climsoft.schemas import paperarchivedefinition_schema
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


@router.get("/paper-archive-definitions", response_model=paperarchivedefinition_schema.PaperArchiveDefinitionResponse)
def get_paper_archive_definitions(
        form_id: str = None,
        description: str = None,
        limit: int = 25,
        offset: int = 0,
        db_session: Session = Depends(get_db)
):
    try:
        paper_archive_definitions = paperarchivedefinition_service.query(
            db_session=db_session,
            form_id=form_id,
            description=description,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=paper_archive_definitions, message="Successfully fetched paper_archive_definitions.")
    except paperarchivedefinition_service.FailedGettingPaperArchiveDefinitionList as e:
        return get_error_response(message=str(e))


@router.get("/paper-archive-definitions/{form_id}", response_model=paperarchivedefinition_schema.PaperArchiveDefinitionResponse)
def get_paper_archive_definition_by_id(form_id: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[paperarchivedefinition_service.get(db_session=db_session, form_id=form_id)],
            message="Successfully fetched paper_archive_definition."
        )
    except paperarchivedefinition_service.FailedGettingPaperArchiveDefinition as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/paper-archive-definitions", response_model=paperarchivedefinition_schema.PaperArchiveDefinitionResponse)
def create_paper_archive_definition(data: paperarchivedefinition_schema.CreatePaperArchiveDefinition, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[paperarchivedefinition_service.create(db_session=db_session, data=data)],
            message="Successfully created paper_archive_definition."
        )
    except paperarchivedefinition_service.FailedCreatingPaperArchiveDefinition as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/paper-archive-definitions/{form_id}", response_model=paperarchivedefinition_schema.PaperArchiveDefinitionResponse)
def update_paper_archive_definition(form_id: str, data: paperarchivedefinition_schema.UpdatePaperArchiveDefinition, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[paperarchivedefinition_service.update(db_session=db_session, form_id=form_id, updates=data)],
            message="Successfully updated paper_archive_definition."
        )
    except paperarchivedefinition_service.FailedUpdatingPaperArchiveDefinition as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/paper-archive-definitions/{form_id}", response_model=paperarchivedefinition_schema.PaperArchiveDefinitionResponse)
def delete_paper_archive_definition(form_id: str, db_session: Session = Depends(get_db)):
    try:
        paperarchivedefinition_service.delete(db_session=db_session, form_id=form_id)
        return get_success_response(
            result=[],
            message="Successfully deleted paper_archive_definition."
        )
    except paperarchivedefinition_service.FailedDeletingPaperArchiveDefinition as e:
        return get_error_response(
            message=str(e)
        )






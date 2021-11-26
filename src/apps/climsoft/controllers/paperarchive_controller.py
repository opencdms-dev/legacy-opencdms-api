from fastapi import APIRouter, Depends
from src.apps.climsoft.services import paperarchive_service
from src.apps.climsoft.schemas import paperarchive_schema
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


@router.get("/paper-archives", response_model=paperarchive_schema.PaperArchiveResponse)
def get_paper_archives(
    belongs_to: str = None,
    form_datetime: str = None,
    image: str = None,
    classified_into: str = None,
    limit: int = 25,
    offset: int = 0,
    db_session: Session = Depends(get_db)
):
    try:
        paper_archives = paperarchive_service.query(
            db_session=db_session,
            belongs_to=belongs_to,
            form_datetime=form_datetime,
            image=image,
            classified_into=classified_into,
            limit=limit,
            offset=offset
        )

        return get_success_response(result=paper_archives, message="Successfully fetched paper_archives.")
    except paperarchive_service.FailedGettingPaperArchiveList as e:
        return get_error_response(message=str(e))


@router.get("/paper-archives/{belongs_to}/{form_datetime}/{classified_into}", response_model=paperarchive_schema.PaperArchiveWithStationAndPaperArchiveDefinitionResponse)
def get_paper_archive_by_id(belongs_to: str, form_datetime: str, classified_into: str, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[paperarchive_service.get(db_session=db_session, belongs_to=belongs_to, form_datetime=form_datetime, classified_into=classified_into)],
            message="Successfully fetched paper_archive."
        )
    except paperarchive_service.FailedGettingPaperArchive as e:
        return get_error_response(
            message=str(e)
        )


@router.post("/paper-archives", response_model=paperarchive_schema.PaperArchiveResponse)
def create_paper_archive(data: paperarchive_schema.CreatePaperArchive, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[paperarchive_service.create(db_session=db_session, data=data)],
            message="Successfully created paper_archive."
        )
    except paperarchive_service.FailedCreatingPaperArchive as e:
        return get_error_response(
            message=str(e)
        )


@router.put("/paper-archives/{belongs_to}/{form_datetime}/{classified_into}", response_model=paperarchive_schema.PaperArchiveResponse)
def update_paper_archive(belongs_to: str, form_datetime: str, classified_into: str, data: paperarchive_schema.UpdatePaperArchive, db_session: Session = Depends(get_db)):
    try:
        return get_success_response(
            result=[paperarchive_service.update(db_session=db_session, belongs_to=belongs_to, form_datetime=form_datetime, classified_into=classified_into, data=data)],
            message="Successfully updated paper_archive."
        )
    except paperarchive_service.FailedUpdatingPaperArchive as e:
        return get_error_response(
            message=str(e)
        )


@router.delete("/paper-archives/{belongs_to}/{form_datetime}/{classified_into}", response_model=paperarchive_schema.PaperArchiveResponse)
def delete_paper_archive(belongs_to: str, form_datetime: str, classified_into: str, db_session: Session = Depends(get_db)):
    try:
        paperarchive_service.delete(db_session=db_session, belongs_to=belongs_to, form_datetime=form_datetime, classified_into=classified_into)
        return get_success_response(
            result=[],
            message="Successfully deleted paper_archive."
        )
    except paperarchive_service.FailedDeletingPaperArchive as e:
        return get_error_response(
            message=str(e)
        )






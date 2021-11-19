import logging
import datetime
import uuid

from passlib.hash import django_pbkdf2_sha256 as handler
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from src.apps.auth.schemas import auth_schema
from src.apps.auth.services import user_service
from src.apps.auth.db.engine import SessionLocal
from src.utils import response
from jose import jwt
from src.config import app_config


router = APIRouter(
    prefix="/api/auth/v1",
    tags=["auth"]
)

logger = logging.getLogger("AuthController")
logging.basicConfig(level=logging.INFO)


async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sign-up")
def sign_up(data: auth_schema.SignUpRequest, db_session: Session = Depends(get_db)):
    try:
        user_service.create(db_session=db_session, data=data)
        return response.get_success_response(result=[], message="Signed up successfully.")
    except Exception as e:
        logger.error(str(e))
        return response.get_error_response(message=str(e))


@router.post("/sign-in")
def sign_in(data: auth_schema.SignInRequest, db_session: Session = Depends(get_db)):
    try:
        user = user_service.get(db_session=db_session, username=data.username)
        if not handler.verify(data.password, user.password):
            raise HTTPException(400, "Invalid login credentials")

        access_token = jwt.encode(
            {
                "sub": user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                "token_type": "access",
                "jti": uuid.uuid4().hex,
                "user_id": int(user.id),
            },
            key=app_config.APP_SECRET,
        )
        return auth_schema.SignInSuccessResponse(access_token=access_token)
    except Exception as e:
        logger.error(str(e))
        return response.get_error_response(message=str(e))











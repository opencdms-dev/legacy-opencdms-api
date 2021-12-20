import logging

from sqlalchemy.orm import Session
from apps.auth.schemas import auth_schema
from fastapi.exceptions import HTTPException
from apps.auth.db.models import user_model
from passlib.hash import django_pbkdf2_sha256 as handler

logger = logging.getLogger("AuthServiceLogger")
logging.basicConfig(level=logging.INFO)


class FailedCreatingUser(Exception):
    pass


class FailedGettingUser(Exception):
    pass


def create(db_session: Session, data: auth_schema.SignUpRequest):
    try:
        existing_user = db_session.query(user_model.AuthUser) \
            .filter(user_model.AuthUser.username == data.username) \
            .one_or_none()

        if existing_user:
            raise HTTPException(409, "User with username already exists")
        user = user_model.AuthUser(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            username=data.username,
            password=handler.hash(data.password)
        )
        db_session.add(user)
        db_session.commit()
    except HTTPException as e:
        raise
    except Exception as e:
        logger.exception(e)
        db_session.rollback()
        raise FailedCreatingUser("Failed creating user.")


def get(db_session: Session, username: str):
    try:
        user = (
            db_session.query(user_model.AuthUser).filter(user_model.AuthUser.username == username).one_or_none()
        )
    except Exception as e:
        raise FailedGettingUser("Failed getting user.")

    if user is None:
        raise HTTPException(400, "Invalid login credentials")

    return user

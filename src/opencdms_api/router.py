from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import text as sa_text
from sqlalchemy.orm.session import Session
from passlib.hash import django_pbkdf2_sha256 as handler
from src.opencdms_api import deps, models
from src.opencdms_api.schema import (
    UserCreateSchema,
    AuthenticationSchema,
    TokenSchema,
    ClimsoftTokenSchema
)
from src.opencdms_api.config import settings
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/users", status_code=201)
def register_new_user(
    payload: UserCreateSchema,
    session: Session = Depends(deps.get_session),
):
    existing_user = (
        session.query(models.AuthUser)
        .filter(models.AuthUser.username == payload.username)
        .one_or_none()
    )
    if existing_user:
        raise HTTPException(409, "User with username already exists")
    user = models.AuthUser(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        username=payload.username,
        password=handler.hash(payload.password),
        is_active=True,
    )
    session.add(user)
    session.commit()


@router.post("/auth", response_model=TokenSchema)
def authenticate(
    payload: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(deps.get_session)
):
    user = (
        session.query(models.AuthUser)
        .filter(models.AuthUser.username == payload.username)
        .one_or_none()
    )
    if user is None:
        raise HTTPException(400, "Invalid login credentials")
    if not handler.verify(payload.password, user.password):
        raise HTTPException(400, "Invalid login credentials")
    access_token = jwt.encode(
        {
            "sub": user.username,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "token_type": "access",
            "jti": str(uuid4()),
            "user_id": int(user.id)
        },
        key=settings.SURFACE_SECRET_KEY,
    )
    return TokenSchema(access_token=access_token, first_name=user.first_name, last_name=user.last_name)


@router.post("/climsoft-auth", response_model=TokenSchema)
def authenticate(
    payload: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_climsoft_session())
):
    user = session.execute(sa_text(f'''
        SELECT User
        FROM mysql.user 
        WHERE User="{payload.username}" AND Password=password("{payload.password}")
    ''')).all()

    if not user:
        raise HTTPException(400, "Invalid login credentials")

    user = user[0]

    access_token = jwt.encode(
        {
            "sub": user[1],
            "exp": datetime.utcnow() + timedelta(hours=24),
            "token_type": "access",
            "jti": str(uuid4()),
            "user_id": int(user.id)
        },
        key=settings.SURFACE_SECRET_KEY,
    )
    return ClimsoftTokenSchema(access_token=access_token, username=user[1])


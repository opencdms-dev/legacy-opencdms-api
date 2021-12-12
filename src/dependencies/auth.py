from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import app_config
from apps.auth.services import user_service
from apps.auth.db.engine import SessionLocal
from apps.auth.schemas import auth_schema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/v1/sign-in")
ALGORITHM = "HS256"


async def get_current_user(token: str = Depends(oauth2_scheme)):
    db_session = SessionLocal()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, app_config.APP_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            db_session.close()
            raise credentials_exception
    except JWTError:
        db_session.close()
        raise credentials_exception
    user = user_service.get(db_session, username=username)
    if user is None:
        db_session.close()
        raise credentials_exception
    db_session.close()
    return user

#
# async def get_current_active_user(current_user=Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user



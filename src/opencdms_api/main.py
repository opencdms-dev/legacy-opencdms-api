import copy
import logging
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from starlette.middleware.wsgi import WSGIMiddleware
from climsoft_api.main import get_app as get_climsoft_app
from climsoft_api.config import settings as climsoft_settings
from tempestas_api.wsgi import application as surface_application
from mch_api.api_mch import app as mch_api_application
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm.session import Session
from passlib.hash import django_pbkdf2_sha256 as handler
from src.opencdms_api.middleware import AuthMiddleWare
from src.opencdms_api.db import SessionLocal
from src.opencdms_api import models
from src.opencdms_api.router import router
from src.opencdms_api.config import settings
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from pygeoapi.flask_app import APP as pygeoapi_app
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from opencdms.models.climsoft import v4_1_1_core as climsoft_models
from src.opencdms_api.middleware import get_authorized_climsoft_user
from climsoft_api.api import api_routers
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


# load controllers
def get_app():
    app = FastAPI(
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"]
            )
        ]
    )
    climsoft_app = get_climsoft_app()

    if settings.SURFACE_API_ENABLED is True:
        surface_wsgi_app = WSGIMiddleware(surface_application)
        app.mount("/surface", surface_wsgi_app)

    if settings.MCH_API_ENABLED is True:
        mch_wsgi_app = WSGIMiddleware(mch_api_application)
        app.mount("/mch", AuthMiddleWare(mch_wsgi_app))

    if settings.CLIMSOFT_API_ENABLED is True:
        for r in api_routers:
            climsoft_app.include_router(
                **r.dict(),
                dependencies=[
                    Depends(oauth2_scheme)
                ]
            )
        app.mount("/climsoft", climsoft_app)

    pygeoapi_wsgi_app = WSGIMiddleware(pygeoapi_app)
    app.mount("/pygeoapi", AuthMiddleWare(pygeoapi_wsgi_app))

    app.include_router(router)

    @app.on_event("startup")
    def create_default_user():
        session: Session = SessionLocal()
        try:
            default_user = (
                session.query(models.AuthUser)
                .filter(models.AuthUser.username == settings.DEFAULT_USERNAME)
                .one_or_none()
            )
            if default_user is None:
                default_user = models.AuthUser(
                    first_name="Default",
                    last_name="User",
                    email="admin@opencdms.org",
                    username=settings.DEFAULT_USERNAME,
                    password=handler.hash(settings.DEFAULT_PASSWORD),
                    is_active=True,
                )
                session.add(default_user)
                session.commit()
            else:
                default_user.password = handler.hash(settings.DEFAULT_PASSWORD)
                session.commit()
        except Exception as e:
            session.rollback()
            logging.getLogger("OpenCDMSLogger").exception(e)
        finally:
            session.close()

        if settings.CLIMSOFT_API_ENABLED:
            climsoft_engine = create_engine(os.getenv("CLIMSOFT_DATABASE_URI"))
            ClimsoftSessionLocal = sessionmaker(climsoft_engine)
            session = ClimsoftSessionLocal()
            try:
                clim_user_role = session.query(
                    climsoft_models.ClimsoftUser
                ).filter_by(
                    userName=settings.DEFAULT_USERNAME
                ).one_or_none()

                if clim_user_role is None:
                    clim_user_role = climsoft_models.ClimsoftUser(
                        userName=settings.DEFAULT_USERNAME,
                        userRole="ClimsoftAdmin"
                    )
                    session.add(clim_user_role)
                    session.commit()
            except Exception as e:
                session.rollback()
                logging.getLogger("OpenCDMSLogger").exception(e)
            finally:
                session.close()

            session.close()

    return app


app = get_app()

path_to_templates = Path(__file__).parents[0] / "templates"
templates = Jinja2Templates(directory=str(path_to_templates.absolute()))


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    supported_apis = [{"title": "Pygeoapi", "url": "/pygeoapi"}]
    if settings.SURFACE_API_ENABLED:
        supported_apis.append({"title": "Surface API", "url": "/surface"})
    if settings.CLIMSOFT_API_ENABLED:
        supported_apis.append({"title": "Climsoft API", "url": "/climsoft"})
    if settings.MCH_API_ENABLED:
        supported_apis.append({"title": "MCH API", "url": "/mch"})
    return templates.TemplateResponse(
        "index.html", {"request": request, "supported_apis": supported_apis}
    )

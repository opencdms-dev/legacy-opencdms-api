from starlette.middleware.wsgi import WSGIMiddleware
from typing import List
from opencdms.models.climsoft.v4_1_1_core import Station
from climsoft_api.main import get_app as get_climsoft_app
from tempestas_api.wsgi import application as surface_application
from mch_api.api_mch import app as mch_api_application
from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm.session import Session
from passlib.hash import django_pbkdf2_sha256 as handler
from src.opencdms_api.middelware import AuthMiddleWare
from src.opencdms_api.schema import StationSchema
from src.opencdms_api.deps import get_session
from src.opencdms_api.db import SessionLocal
from src.opencdms_api import models
from src.opencdms_api.router import router
from src.opencdms_api.config import settings
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from pygeoapi.flask_app import APP as pygeoapi_app
from fastapi.middleware.cors import CORSMiddleware


# load controllers
def get_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    climsoft_app = get_climsoft_app()
    if settings.SURFACE_API_ENABLED is True:
        app.mount("/surface", AuthMiddleWare(WSGIMiddleware(surface_application)))
    if settings.MCH_API_ENABLED is True:
        app.mount("/mch", AuthMiddleWare(WSGIMiddleware(mch_api_application)))
    if settings.CLIMSOFT_API_ENABLED is True:
        app.mount("/climsoft", AuthMiddleWare(climsoft_app))
    app.mount("/pygeoapi", AuthMiddleWare(WSGIMiddleware(pygeoapi_app)))

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
                    email="admin@opencdms_api.com",
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
            raise e
        finally:
            session.close()

    return app


app = get_app()

path_to_templates = Path(__file__).parents[0] / "templates"
templates = Jinja2Templates(directory=str(path_to_templates.absolute()))


@app.get("/stations", response_model=List[StationSchema])
def fetch_stations(session: Session = Depends(get_session)):
    return session.query(Station).all()


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

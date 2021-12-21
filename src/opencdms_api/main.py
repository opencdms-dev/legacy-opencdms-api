from starlette.middleware.wsgi import WSGIMiddleware
from typing import List
from opencdms.models.climsoft.v4_1_1_core import Station
from apps.climsoft.main import app as climsoft_app
from tempestas_api.wsgi import application as surface_application
from mch_api.api_mch import app as mch_api_application
from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session

from opencdms_api.middelware import AuthMiddleWare
from opencdms_api.schema import StationSchema
from opencdms_api.deps import get_session
from opencdms_api.router import router
# from pygeoapi.starlette_app import app as pygeoapi_app
from pygeoapi.flask_app import APP as pygeoapi_app

# load controllers


def get_app():
    app = FastAPI()
    # climsoft_app.add_middleware(AuthMiddleWare)
    app.mount("/surface", AuthMiddleWare(WSGIMiddleware(surface_application)))
    app.mount("/mch", AuthMiddleWare(WSGIMiddleware(mch_api_application)))
    app.mount("/climsoft", climsoft_app)
    app.mount("/pygeoapi", WSGIMiddleware(pygeoapi_app))
    app.include_router(router)
    return app


app = get_app()


@app.get("/stations", response_model=List[StationSchema])
def fetch_stations(session: Session = Depends(get_session)):
    return session.query(Station).all()

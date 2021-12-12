from starlette.middleware.wsgi import WSGIMiddleware
from typing import List
from opencdms.models.climsoft.v4_1_1_core import Station
from tempestas_api.wsgi import application as surface_application
from mch_api.api_mch import app as mch_api_application
from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session

from opencdms_api.middelware import WSGIAuthMiddleWare
from opencdms_api.schema import StationSchema
from opencdms_api.deps import get_session
from opencdms_api.router import router


# load controllers

def get_app():
    app = FastAPI()
    app.mount("/surface", WSGIAuthMiddleWare(WSGIMiddleware(surface_application)))
    app.mount("/mch", WSGIAuthMiddleWare(WSGIMiddleware(mch_api_application)))
    app.include_router(router)
    return app


app = get_app()


@app.get("/stations", response_model=List[StationSchema])
def fetch_stations(session: Session = Depends(get_session)):
    return session.query(Station).all()

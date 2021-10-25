# import sys
# import os
# from pathlib import Path

# surface_path = Path(__file__).parents[2] / "surface/api"
# sys.path.append(str(surface_path))
# print("\n\n\n\n\n\n")
# print(sys.path)
# print(os.getenv('PYTHONPATH'))
# print("\n\n\n\n\n\n")



from starlette.middleware.wsgi import WSGIMiddleware
from typing import List
from opencdms.models.climsoft.v4_1_1_core import Station
from surface.api.tempestas_api.wsgi import application as surface_application

from mch_api.api_mch import app as mch_api_application
from fastapi import FastAPI, Depends
from sqlalchemy.orm.session import Session

from opencdms_server.middelware import WSGIAuthMiddleWare
from opencdms_server.schema import StationSchema
from opencdms_server.deps import get_session




app = FastAPI()

app.mount("/surface", WSGIAuthMiddleWare(WSGIMiddleware(surface_application)))
app.mount("/mch", WSGIAuthMiddleWare(WSGIMiddleware(mch_api_application)))


@app.get("/stations", response_model=List[StationSchema])
def fetch_stations(session: Session = Depends(get_session)):
    return session.query(Station).all()

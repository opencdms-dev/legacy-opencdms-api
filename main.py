import uvicorn
import os
from typing import List
from opencdms.models.climsoft.v4_1_1_core import Station
from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from pydantic import BaseModel

app = FastAPI()

database_url = os.getenv("DATABASE_URI")
engine = create_engine(database_url)


SessionLocal = sessionmaker(engine)


class StationSchema(BaseModel):
    """Station response schema"""

    stationId: str
    stationName: str
    wmoid: str
    icaoid: str
    latitude: float
    qualifier: str
    longitude: float
    elevation: str
    geoLocationMethod: str
    geoLocationAccuracy: float
    openingDatetime: str
    closingDatetime: str
    country: str
    authority: str
    adminRegion: str
    drainageBasin: str
    wacaSelection: int
    cptSelection: int
    stationOperational: int

    class Config:
        orm_mode = True


def get_session():
    """
    Api dependency to provide database session to a request
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


@app.get("/stations", response_model=List[StationSchema])
def fetch_stations(session: Session = Depends(get_session)):
    return session.query(Station).all()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")

from pydantic.networks import EmailStr
import inflection
from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        alias_generator = lambda x: inflection.camelize(x, False)  # noqa
        allow_population_by_field_name = True


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


class UserCreateSchema(BaseSchema):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str


class AuthenticationSchema(BaseSchema):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str

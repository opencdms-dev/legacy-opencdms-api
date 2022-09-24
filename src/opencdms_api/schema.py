from fastapi import Form
from typing import Optional
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
    first_name: str
    last_name: str


class ClimsoftTokenSchema(BaseModel):
    access_token: str
    username: str


class CurrentUserSchema(BaseSchema):
    email: EmailStr
    username: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class CurrentClimsoftUserSchema(BaseModel):
    username: str
    deployment_key: str = None


class ClimsoftPasswordRequestForm:
    def __init__(
        self,
        grant_type: str = Form(None, regex="password"),
        username: str = Form(...),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scope = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret

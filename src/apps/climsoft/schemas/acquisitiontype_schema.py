from typing import List
from pydantic import BaseModel
from common_schemas import Response


class CreateAcquisitionType(BaseModel):
    code: int
    description: str


class UpdateAcquisitionType(BaseModel):
    description: str


class AcquisitionType(CreateAcquisitionType):

    class Config:
        orm_mode = True


class AcquisitionTypeResponse(Response):
    result: List[AcquisitionType]



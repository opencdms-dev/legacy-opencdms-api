from pydantic import BaseModel


class CreateAcquisitionType(BaseModel):
    code: int
    description: str


class UpdateAcquisitionType(BaseModel):
    description: str


class AcquisitionType(CreateAcquisitionType):

    class Config:
        orm_mode = True




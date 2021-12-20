from pydantic import BaseModel, constr
from typing import List
from common_schemas import Response


class CreateRegKey(BaseModel):
    keyName: constr(max_length=255)
    keyValue: constr(max_length=255)
    keyDescription: constr(max_length=255)

    class Config:
        fields = {
            "keyName": "key_name",
            "keyValue": "key_value",
            "keyDescription": "key_description"
        }


class UpdateRegKey(BaseModel):
    keyValue: constr(max_length=255)
    keyDescription: constr(max_length=255)

    class Config:
        fields = {
            "keyValue": "key_value",
            "keyDescription": "key_description"
        }


class RegKey(CreateRegKey):
    class Config:
        fields = {
            "keyName": "key_name",
            "keyValue": "key_value",
            "keyDescription": "key_description"
        }
        orm_mode = True
        allow_population_by_field_name = True


class RegKeyResponse(Response):
    result: List[RegKey]









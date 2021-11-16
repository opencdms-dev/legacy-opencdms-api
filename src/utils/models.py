import inspect
import json

from pydantic import BaseModel, validator
from pydantic.class_validators import Validator


def extract_validators(model):
    return {name: extract_validator_function_name(func[0]) for name, func in model.__validators__.items()}


def extract_validator_function_name(validator_func: Validator):
    return next(filter(lambda x: inspect.isfunction(x[1]), inspect.getmembers(validator_func)))[1].__name__


def generate_schema_with_validators(model):
    return {**model.schema(), "validators": extract_validators(model=model)}


if __name__ == "__main__":
    class UserModel(BaseModel):
        name: str
        username: str
        password1: str
        password2: str

        @validator('name')
        def name_must_contain_space(cls, v):
            if ' ' not in v:
                raise ValueError('must contain a space')
            return v.title()

        @validator('password2')
        def passwords_match(cls, v, values, **kwargs):
            if 'password1' in values and v != values['password1']:
                raise ValueError('passwords do not match')
            return v

        @validator('username')
        def username_alphanumeric(cls, v):
            assert v.isalnum(), 'must be alphanumeric'
            return v


    print(json.dumps(generate_schema_with_validators(UserModel), indent=2))

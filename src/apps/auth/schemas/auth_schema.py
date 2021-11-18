from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str


class SignInRequest(BaseModel):
    username: str
    password: str


class SignInSuccessResponse(BaseModel):
    access_token: str



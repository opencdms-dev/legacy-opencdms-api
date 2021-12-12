from faker import Faker
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.apps.auth.schemas import auth_schema


fake = Faker()


def get_valid_signup_input():
    return auth_schema.SignUpRequest(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        password="password",
        email=fake.email()
    )


def get_valid_signin_input(username: str, password: str = "password"):
    return OAuth2PasswordRequestForm(
        username=username,
        password=password,
        scope=""
    )

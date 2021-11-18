from faker import Faker
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
    return auth_schema.SignInRequest(
        username=username,
        password=password
    )

import os

from pydantic import BaseSettings


os.environ["AUTH_ENABLED"] = "False"


class Settings(BaseSettings):
    AUTH_ENABLED: bool


if __name__ == "__main__":
    settings = Settings()

    print(type(settings.AUTH_ENABLED))

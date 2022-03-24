from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    SECRET_KEY: str

    SURFACE_SECRET_KEY: str

    SURFACE_DB_HOST: str
    SURFACE_DB_PORT: str
    SURFACE_DB_NAME: str
    SURFACE_DB_USER: str
    SURFACE_DB_PASSWORD: str

    SURFACE_API_ENABLED: bool
    CLIMSOFT_API_ENABLED: bool
    MCH_API_ENABLED: bool

    DEFAULT_USERNAME: str
    DEFAULT_PASSWORD: str

    AUTH_ENABLED: bool

    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any]  # noqa
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("SURFACE_DB_USER"),
            password=values.get("SURFACE_DB_PASSWORD"),
            host=values.get("SURFACE_DB_HOST"),
            port=values.get("SURFACE_DB_PORT"),
            path=f"/{values.get('SURFACE_DB_NAME') or ''}",
        )

    class Config:
        case_sensitive = True
        env_file_encoding = "utf-8"


settings = Settings()

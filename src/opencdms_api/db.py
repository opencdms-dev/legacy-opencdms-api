import os
from contextlib import contextmanager
from src.opencdms_api.config import settings
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import Generator
from sqlalchemy.ext.declarative import declarative_base
from src.opencdms_api.utils.multi_deployment import load_deployment_configs

engine = create_engine(settings.DATABASE_URI)
SessionLocal = sessionmaker(engine)
Base = declarative_base()

ScopedSession = scoped_session(SessionLocal)


def get_climsoft_engine(deployment_key):
    deployment_configs = load_deployment_configs()
    if deployment_key and deployment_configs[deployment_key].get("DATABASE_URI"):
        return create_engine(deployment_configs[deployment_key].get("DATABASE_URI"))
    else:
        return create_engine(os.getenv("CLIMSOFT_DATABASE_URI"))


def get_climsoft_session_local(deployment_key: str = None):
    return sessionmaker(get_climsoft_engine(deployment_key))


@contextmanager
def db_session_scope(bind: Engine = None) -> Generator[Session, None, None]:
    try:
        if bind:
            yield ScopedSession(bind=bind)
        else:
            yield ScopedSession()
        ScopedSession.commit()
    except Exception:
        ScopedSession.rollback()
        raise
    finally:
        ScopedSession.remove()

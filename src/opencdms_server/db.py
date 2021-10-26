from contextlib import contextmanager
from opencdms_server.config import settings
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import Generator
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(settings.DATABASE_URI)


SessionLocal = sessionmaker(engine)

Base = declarative_base()

ScopedSession = scoped_session(SessionLocal)


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

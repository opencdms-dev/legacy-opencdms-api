from sqlalchemy.orm.session import Session
from src.opencdms_api.db import SessionLocal, get_climsoft_session_local


def get_session():
    """
    Api dependency to provide database session to a request
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_climsoft_session(deployment_key: str = None):
    """
    Api dependency to provide climsoft database session to a request
    """
    return get_climsoft_session_local(deployment_key)()

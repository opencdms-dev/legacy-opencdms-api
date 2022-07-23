from sqlalchemy.orm.session import Session
from src.opencdms_api.db import SessionLocal, ClimsoftSessionLocal


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


def get_climsoft_session():
    """
    Api dependency to provide climsoft database session to a request
    """
    session: Session = ClimsoftSessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


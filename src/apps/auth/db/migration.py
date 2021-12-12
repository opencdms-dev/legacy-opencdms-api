from src.apps.auth.db import engine
from src.apps.auth.db.models.user_model import Base


def migrate():
    Base.metadata.create_all(engine.db_engine)

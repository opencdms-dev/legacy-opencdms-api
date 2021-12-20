from apps.auth.db import engine
from apps.auth.db.models.user_model import Base


def migrate():
    Base.metadata.create_all(engine.db_engine)

from opencdms.models.climsoft.v4_1_1_core import Base
from src.apps.climsoft.db import engine


def migrate():
    Base.metadata.create_all(engine.db_engine)

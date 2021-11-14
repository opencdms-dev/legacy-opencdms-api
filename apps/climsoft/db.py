from opencdms.models.climsoft.v4_1_1_core import Base
from fastapi_sqlalchemy import db
from sqlalchemy.engine import Engine


def migrate(engine: Engine):
    with db():
        Base.metadata.create_all(engine)

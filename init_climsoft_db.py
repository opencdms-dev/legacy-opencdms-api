from opencdms.models.climsoft.v4_1_1_core import Base
from climsoft_api.db import engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)

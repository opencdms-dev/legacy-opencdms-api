import os
from sqlalchemy import create_engine


db_url = os.getenv("DATABASE_URI", "mysql+mysqldb://root:password@192.168.0.104:33308/climsoft_dev")
db_engine = create_engine(db_url)


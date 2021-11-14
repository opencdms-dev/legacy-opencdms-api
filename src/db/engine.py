import os
from sqlalchemy import create_engine


db_url = os.getenv("DATABASE_URI", "mysql+mysqldb://root:password@127.0.0.1:33308/climsoft_dev")
db_engine = create_engine(db_url)


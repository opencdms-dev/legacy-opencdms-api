from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import app_config


db_engine = create_engine(
    app_config.AUTH_DB_URI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)




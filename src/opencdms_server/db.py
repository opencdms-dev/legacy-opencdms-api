from opencdms_server.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine(settings.DATABASE_URI)


SessionLocal = sessionmaker(engine)

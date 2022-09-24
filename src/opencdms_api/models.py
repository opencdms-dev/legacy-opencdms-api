from sqlalchemy.sql.sqltypes import Boolean
from src.opencdms_api.db import Base
from sqlalchemy import Sequence, Column, Integer, String, DateTime, func


class AuthUser(Base):
    """Auth user model defined to match that of surface db"""

    __tablename__ = "auth_user"
    # __table_args__ = (UniqueConstraint("org_id", "datasource_id"),)
    auth_user_id_seq = Sequence("auth_user_id_seq", metadata=Base.metadata)
    id = Column(Integer, primary_key=True, server_default=auth_user_id_seq.next_value())
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, nullable=False, default=True)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False)
    date_joined = Column(DateTime, nullable=False, default=func.now())

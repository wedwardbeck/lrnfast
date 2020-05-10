from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_date = Column(DateTime, server_default=func.now(), nullable=False)


# from sqlalchemy import Boolean, Column, DateTime, Integer, String, Table, func
#
# from app.db.session import metadata
#
# user = Table(
#     "user",
#     metadata,
#     Column("id", Integer, primary_key=True, index=True),
#     Column("full_name", String, index=True),
#     Column("email", String, unique=True, index=True),
#     Column("hashed_password", String),
#     Column("is_active", Boolean(), default=True),
#     Column("is_superuser", Boolean(), default=False),
#     Column("created_date", DateTime, server_default=func.now(), nullable=False),
# )

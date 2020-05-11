import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func

from app.db.base_class import Base


class Note(Base):

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    description = Column(String(50), index=True)
    created_date = Column(DateTime, server_default=func.now(), nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
    changed_date = Column(DateTime, onupdate=datetime.datetime.now)
    changed_by = Column(Integer, ForeignKey("user.id"))

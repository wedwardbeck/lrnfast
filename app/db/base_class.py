import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase(object):
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # @declared_attr
    # def owner_id(cls):
    #     return Column(Integer, ForeignKey("user.id"))
    #
    # @declared_attr
    # def changed_by(cls):
    #     return Column(Integer, ForeignKey("user.id"))

    # @declared_attr
    # def created_on(cls):
    #     return Column(DateTime, default=datetime.datetime.now)
    #
    # @declared_attr
    # def changed_on(cls):
    #     return Column(DateTime, onupdate=datetime.datetime.now)
    #
    # _creation_order = 9999


Base = declarative_base(cls=CustomBase)

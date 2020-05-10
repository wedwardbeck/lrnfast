from databases import Database
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core import config

database = Database(config.SQLALCHEMY_DATABASE_URI)
metadata = MetaData()

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

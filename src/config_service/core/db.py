import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv('REGISTRY_URL')

engine = create_engine(DATABASE_URL, convert_unicode=True)

# Create a scoped session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class for models
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from . import base
    Base.metadata.create_all(bind=engine)

def shutdown_session(exception=None):
    db_session.remove()

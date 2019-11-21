
import uuid
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, String, DateTime, func, desc
from sqlalchemy.ext.declarative import declarative_base
from flask_jsontools import JsonSerializableBase

def generateId():
    return str(uuid.uuid4())

class MyBaseClass:

    id = Column(String, primary_key=True, default=generateId)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, onupdate=func.now())
    deleted = Column(DateTime)

    def __init__(self):
        self.id = generateId()

#Base = declarative_base(cls=(JsonSerializableBase,MyBaseClass))
Base = declarative_base(cls=MyBaseClass)

def crear_tablas():
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['DB_USER'],
        os.environ['DB_PASSWORD'],
        os.environ['DB_HOST'],
        os.environ.get('DB_PORT',5432),
        os.environ['DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)

import os
import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model_utils import Base
from .entities import *

port = os.environ.get('SILEG_DB_PORT', '5432')

@contextlib.contextmanager
def obtener_session(echo=False):
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['SILEG_DB_USER'],
        os.environ['SILEG_DB_PASSWORD'],
        os.environ['SILEG_DB_HOST'],
        port,
        os.environ['SILEG_DB_NAME']
    ), echo=echo)

    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()

from .SilegModel import SilegModel

__all__ = [
    'SilegModel'
]

def crear_tablas():
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
        os.environ['SILEG_DB_USER'],
        os.environ['SILEG_DB_PASSWORD'],
        os.environ['SILEG_DB_HOST'],
        port,
        os.environ['SILEG_DB_NAME']
    ), echo=True)
    Base.metadata.create_all(engine)

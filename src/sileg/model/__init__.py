import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model_utils import Base
from .entities import *

port = os.environ.get('SILEG_DB_PORT', '5432')
engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
    os.environ['SILEG_DB_USER'],
    os.environ['SILEG_DB_PASSWORD'],
    os.environ['SILEG_DB_HOST'],
    port,
    os.environ['SILEG_DB_NAME']
), echo=True)
Session = sessionmaker(bind=engine)



from .SilegModel import SilegModel

__all__ = [
    'SilegModel'
]

def crear_tablas():
    Base.metadata.create_all(engine)

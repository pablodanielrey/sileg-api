import logging
logging.getLogger().setLevel(logging.DEBUG)

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base

from sileg.model.entities import Lugar, Direccion, CumpleFunciones

engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
    os.environ['SILEG_DB_USER'],
    os.environ['SILEG_DB_PASSWORD'],
    os.environ['SILEG_DB_HOST'],
    os.environ['SILEG_DB_NAME']
), echo=True)

Session = sessionmaker(bind=engine)

s = Session()

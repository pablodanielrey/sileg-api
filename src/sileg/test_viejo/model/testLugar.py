import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base

from sileg.model.entities import Lugar


engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
    os.environ['SILEG_DB_USER'],
    os.environ['SILEG_DB_PASSWORD'],
    os.environ['SILEG_DB_HOST'],
    os.environ['SILEG_DB_NAME']
), echo=True)

#engine.execute(CreateSchema('sileg'))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

s = Session()


l = Lugar()
l.nombre = 'prueba'
s.add(l)

logging.getLogger().setLevel(logging.INFO)
for l in s.query(Lugar).all():
    logging.info(l.__json__())


s.commit()

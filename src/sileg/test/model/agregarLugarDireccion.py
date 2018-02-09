import logging
logging.getLogger().setLevel(logging.DEBUG)

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base

from sileg.model.entities import Lugar, Direccion


if __name__ == '__main__':

    nombre = sys.argv[1]

    engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
        os.environ['SILEG_DB_USER'],
        os.environ['SILEG_DB_PASSWORD'],
        os.environ['SILEG_DB_HOST'],
        os.environ['SILEG_DB_NAME']
    ), echo=True)

    Session = sessionmaker(bind=engine)

    s = Session()


    d = Direccion(nombre)
    s.add(d)
    s.commit()

    logging.info('El id generado es : {}'.format(d.id))

    #for l in s.query(Lugar).all():
    #    logging.info(l.__json__())

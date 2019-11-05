import logging
logging.getLogger().setLevel(logging.DEBUG)

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base

from sileg.model.entities import Lugar, Catedra


if __name__ == '__main__':

    materia_id = sys.argv[1]
    nombre = sys.argv[2] if len(sys.argv) > 2 else 'original'


    engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
        os.environ['SILEG_DB_USER'],
        os.environ['SILEG_DB_PASSWORD'],
        os.environ['SILEG_DB_HOST'],
        os.environ['SILEG_DB_NAME']
    ), echo=True)

    Session = sessionmaker(bind=engine)

    s = Session()


    c = Catedra(nombre)
    c.materia_id = materia_id

    s.add(c)
    s.commit()

    logging.info('El id generado es : {}'.format(c.id))

    #for l in s.query(Lugar).all():
    #    logging.info(l.__json__())

import sys
import logging
logging.getLogger().setLevel(logging.INFO)
import os
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base

from sileg.model.entities import Usuario, Designacion, Cargo, Lugar


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        sys.exit(1)

    engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
        os.environ['SILEG_DB_USER'],
        os.environ['SILEG_DB_PASSWORD'],
        os.environ['SILEG_DB_HOST'],
        os.environ['SILEG_DB_NAME']
    ), echo=False)
    Session = sessionmaker(bind=engine)
    s = Session()

    operacion = sys.argv[1]
    if operacion == 'c':
        #engine.execute(CreateSchema('sileg'))
        Base.metadata.create_all(engine)
        s.commit()

        u = s.query(Usuario).filter_by(id='89d88b81-fbc0-48fa-badb-d32854d3d93a').first()
        if not u:
            u = Usuario(id='89d88b81-fbc0-48fa-badb-d32854d3d93a')
            s.add(u)

        l = Lugar(nombre='casa de ivan')
        s.add(l)

        c = Cargo(nombre='e7')
        s.add(c)

        d = Designacion(usuario=u, lugar=l, cargo=c)
        s.add(d)
        s.commit()


    u = s.query(Usuario).filter_by(id='89d88b81-fbc0-48fa-badb-d32854d3d93a').first()

    for d in s.query(Designacion).all():
        d.usuario = u
        s.commit()

    logging.info('------------------------------------------')
    ''' listo las designaciones con sus datos asociados '''
    for l in s.query(Designacion).all():
        logging.info(l.__json__())
        logging.info(l.cargo.__json__())
        logging.info(l.lugar.__json__())
        logging.info(l.usuario.__json__())

    logging.info('------------------------------------------')
    ''' listo los usuarios con sus designaciones '''
    for u in s.query(Usuario).all():
        logging.info(u.__json__())
        for d in u.designaciones:
            logging.info(d.__json__())

    logging.info('------------------------------------------')
    ''' listo los usuarios con sus cargos '''
    for u in s.query(Usuario).all():
        logging.info(u.__json__())
        for d in u.designaciones:
            logging.info(d.cargo.__json__())

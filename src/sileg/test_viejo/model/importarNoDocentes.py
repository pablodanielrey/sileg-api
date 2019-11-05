import logging
logging.getLogger().setLevel(logging.DEBUG)

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base

from sileg.model.entities import *

if __name__ == '__main__':

    engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
        os.environ['SILEG_DB_USER'],
        os.environ['SILEG_DB_PASSWORD'],
        os.environ['SILEG_DB_HOST'],
        os.environ['SILEG_DB_NAME']
    ))

    Session = sessionmaker(bind=engine)

    s = Session()

    with open('usuarios.csv','r') as f:
        for line in f:
            row = line.split(',')
            uid = row[0]
            dni = row[1]
            oficina = row[4]
            oficinaId = row[5].rstrip('\n')
            # logging.info("Procesando -> Dni: {} Oficina: {} id oficina: {}".format(dni, oficina, oficinaId))
            l = s.query(Lugar).filter(Lugar.id == oficinaId).one_or_none()

            # creo los lugares que no existen
            if l is None:
                logging.info('la oficina {} no existe'.format(oficina))

                if 'departamento' in oficina.strip().lower():
                    lugar = Departamento(nombre=oficina)
                    lugar.id = oficinaId
                    s.add(lugar)
                    s.commit()
                    logging.info("Se creo el departamento: {} id: {}".format(oficina, oficinaId))

                elif 'dirección' in oficina.strip().lower():
                    lugar = Direccion(nombre=oficina)
                    lugar.id = oficinaId
                    s.add(lugar)
                    s.commit()
                    logging.info("Se crea la dirección: {} id: {}".format(oficina, oficinaId))

                elif 'secretaría' in oficina.strip().lower():
                    lugar = Secretaria(nombre=oficina)
                    lugar.id = oficinaId
                    s.add(lugar)
                    s.commit()
                    logging.info("Se crea la secretaría: {} id: {}".format(oficina, oficinaId))

                elif 'centro' in oficina.strip().lower():
                    lugar = Centro(nombre=oficina)
                    lugar.id = oficinaId
                    s.add(lugar)
                    s.commit()
                    logging.info("Se crea el centro : {} id: {}".format(oficina, oficinaId))
                else:
                    lugar = Lugar(nombre=oficina)
                    lugar.id = oficinaId
                    s.add(lugar)
                    s.commit()
                    logging.info("Se crea el lugar: {} id: {}".format(oficina, oficinaId))

            l = s.query(Lugar).filter(Lugar.id == oficinaId).one()

            cf = s.query(Cargo).filter(Cargo.id == '245eae51-28c4-4c6b-9085-354606399666').one()

            u = s.query(Usuario).filter(Usuario.id == uid).one_or_none()
            if u is None:
                logging.info('Creando al usuario {} con id {}'.format(row[2] + ', ' + row[3], uid))
                u = Usuario()
                u.id = uid
                s.add(u)
                s.commit()

            u = s.query(Usuario).filter(Usuario.id == uid).one()

            d = s.query(Designacion).filter(Designacion.usuario_id == uid, Designacion.lugar_id == oficinaId).all()
            if d is None or len(d) < 1:
                logging.info('Creando designacion al usuario {} con id {} al lugar con id {}'.format(dni, uid, l.id))
                d = Designacion()
                d.usuario = u
                d.cargo = cf
                d.lugar = l
                s.add(d)
                s.commit()
            else:
                logging.info('El usuario {} ya posee designacion'.format(dni))

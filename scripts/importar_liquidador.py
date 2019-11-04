import os
import sys
import csv
import uuid
import re
from dateutil.parser import parse
import datetime
import logging
logging.getLogger().setLevel(logging.DEBUG)

from sqlalchemy import and_

from sileg.model.entities import Designacion, Cargo
from sileg.model import obtener_session
from sileg.model.UserCache import UserCache
from sileg.model.API import API



USUARIOS_URL = os.environ['USERS_API_URL']
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

api = API()

def _get_user_uuid(uuid, token=None):
    query = '{}/usuarios/{}'.format(USUARIOS_URL, uuid)
    r = api.get(query, token=token)
    if not r.ok:
        return None
    usr = r.json()        
    return usr

def _get_user_dni(dni, token=None):
    query = '{}/usuarios/'.format(USUARIOS_URL)
    r = api.get(query, params={'q':dni}, token=token)
    if not r.ok:
        return None
    for usr in r.json():
        return usr        
    return None

cache = UserCache(REDIS_HOST, REDIS_PORT, _get_user_uuid, _get_user_dni)

CARGO_CUMPLE_FUNCIONES_NO_DOCENTE = '245eae51-28c4-4c6b-9085-354606399666'
CARGO_CUMPLE_FUNCIONES_DOCENTE = '07bac038-f4a8-437b-843e-607ea89b72e2'

if __name__ == '__main__':

    reg = re.compile('[A|B|C|D|E]+.*')
    
    archivo = sys.argv[1]
    with open(archivo,'r') as f:

        with obtener_session() as s:

            tk = api._get_token()

            c = csv.reader(f, delimiter=',', quotechar="\"")
            for r in c:
                cargo = r[7].strip()

                if cargo == 'Clase Grupo':
                    continue

                dni = r[1].strip().lower()

                #fecha = parse(r[19])
                fecha = datetime.datetime.strptime(r[16], '%Y%m%d')
                n = r[2].split(',')
                nombre = ''
                apellido = ''
                if len(n) >= 2:
                    nombre = n[1].strip().capitalize()
                    apellido = n[0].strip().capitalize()
                else:
                    nombre = n[0].strip().capitalize()

                r = {
                    'cargo': cargo,
                    'dni': dni,
                    'nombre': nombre,
                    'apellido': apellido,
                    'fecha': fecha
                }
                
                m = reg.match(cargo)
                if m:
                    # es no docente
                    logging.debug(r)

                    """
                    _cargo = s.query(Cargo).filter(Cargo.nombre == cargo).one_or_none()
                    if not _cargo:
                        cid = str(uuid.uuid4())
                        s.add(Cargo(id=cid, nombre=cargo, tipo=Cargo._tipos[1]))
                        s.commit()
                    """

                    usr = cache.obtener_usuario_por_dni(dni, tk)
                    uid = usr['id']
                    logging.debug(uid)

                    q = s.query(Designacion).filter(Designacion.usuario_id == uid, Designacion.cargo_id == CARGO_CUMPLE_FUNCIONES_NO_DOCENTE).all()
                    for c in q:
                        if c.historico:
                            continue

                        did = c.id
                        logging.debug(c.__json__())

                        _cargo = s.query(Cargo).filter(Cargo.nombre == cargo).one_or_none()
                        if not _cargo:
                            raise Exception('cargo erroneo')
                        c.cargo_id = _cargo.id
                        c.desde = fecha
                        c.hasta = None
                        s.commit()

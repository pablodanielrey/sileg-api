
import sys
import os
import logging
logging.getLogger().setLevel(logging.INFO)
import re
import json
from dateutil import parser

from sileg.model import obtener_session, SilegModel
from model_utils.API import API
from sileg.model.UsersAPI import UsersAPI

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
USERS_API = os.environ['USERS_API_URL']
OIDC_URL = os.environ['OIDC_URL']
OIDC_CLIENT_ID = os.environ['OIDC_CLIENT_ID']
OIDC_CLIENT_SECRET = os.environ['OIDC_CLIENT_SECRET']


def parsear_r(r):
    return {
        'dni': r[0].replace(' ', ''),
        'nombre': r[1],
        'cargo': r[2].replace(' ', ''),
        'ant': int(r[3])
    }

if __name__ == '__main__':

    with obtener_session() as session:
        cargos = SilegModel.cargos(session)

    desig = {}
    #archivo = sys.argv[1]
    archivo = '/home/pablo/Descargas/liquidador-2018.csv'
    with open(archivo, 'r') as f:
        for reg in f:
            logging.info(reg)
            d = reg.split(',')
            r = parsear_r(d)

            for c in cargos:
                if r['cargo'] == c.nombre:
                    r['cargo_id'] = c.id
                    break

            desig[r['dni']] = r


    agenerar = []
    with obtener_session() as session:
        for did,d in desig.items():
            api = API(url=OIDC_URL,
                    client_id=OIDC_CLIENT_ID, 
                    client_secret=OIDC_CLIENT_SECRET, 
                    verify_ssl=VERIFY_SSL)
            users = UsersAPI(api_url=USERS_API, api=api)

            tk = api._get_token()
            user = users._get_user_dni(dni=d['dni'], token=tk)
            #logging.info(user)
            d['usuario_id'] = user['id']

            designaciones = SilegModel.designaciones(session=session, persona=user['id'])
            if designaciones and len(designaciones) > 0:
                d['lugar_id'] = designaciones[-1].lugar_id
                cargo_a_generar = designaciones[-1].cargo_id

                logging.info('chequeando que {} != {}'.format(d['cargo_id'], cargo_a_generar))
                if d['cargo_id'] != cargo_a_generar:
                    logging.info('agregando persona a cargar')
                    logging.info(d)
                    agenerar.append(d)
            else:
                d['lugar_id'] = '5776a70e-a9af-466d-b9c4-89e646fc39af'
                agenerar.append(d)
    
    logging.info('cantidad: {}'.format(len(agenerar)))

    """ ahora si genero las designaciones correctas con la fecha 01/11/2018 ya que no las tengo dentro del liquidador y es la fecha del listado """

    """
    desde = parser.parse('01/11/2018')
    with obtener_session() as session:
        for did, d in desig.items():
            generada_id = SilegModel.crearDesignacion(session, d['usuario_id'], d['cargo_id'], d['lugar_id'], desde)
            logging.info('designacion generada : {}'.format(d))
    """
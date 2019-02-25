
import sys
import os
import logging
logging.getLogger().setLevel(logging.DEBUG)
import re
import json

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

    for did,d in desig.items():
        api = API(url=OIDC_URL,
                client_id=OIDC_CLIENT_ID, 
                client_secret=OIDC_CLIENT_SECRET, 
                verify_ssl=VERIFY_SSL)
        users = UsersAPI(api_url=USERS_API, api=api)

        tk = api._get_token()
        user = users._get_user_dni(dni=d['dni'], token=tk)
        logging.info(user)
        d['usuario'] = user

        logging.info(d)
    
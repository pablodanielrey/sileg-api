import logging
logging.getLogger().setLevel(logging.INFO)
import os
import csv

from sileg.model import obtener_session, SilegModel
from model_utils.API import API
from sileg.model.UsersAPI import UsersAPI
from sileg.model.GoogleAuthApi import GAuthApis

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
USERS_API = os.environ['USERS_API_URL']
OIDC_URL = os.environ['OIDC_URL']
OIDC_CLIENT_ID = os.environ['OIDC_CLIENT_ID']
OIDC_CLIENT_SECRET = os.environ['OIDC_CLIENT_SECRET']
import warnings

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
admin = os.environ.get('ADMIN_USER_GOOGLE')
google_service = GAuthApis.getServiceAdmin(admin)

def _obtener_usuario_google_id(usuario):
    return '{}@econo.unlp.edu.ar'.format(usuario.dni)

def check_google(usuario):
    usuario_google = '{}@econo.unlp.edu.ar'.format(usuario["dni"])
    logging.info("Chequeando en google el usuario: {}".format(usuario_google))
    try:
        """ https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/admin_directory_v1.users.html """
        u = google_service.users().get(userKey=usuario_google).execute()
        logging.info(u['emails'])
        return u
    except Exception:
        ''' el usuario no existe '''
        logging.info("El usuario no existe")    
        return None

if __name__ == '__main__':
        
    uids = []

    with obtener_session() as session:
        uids = SilegModel.obtener_uids(session)
        
    api = API(url=OIDC_URL,
            client_id=OIDC_CLIENT_ID, 
            client_secret=OIDC_CLIENT_SECRET, 
            verify_ssl=VERIFY_SSL)
    users = UsersAPI(api_url=USERS_API, api=api)
    logging.info(users.url)
    tk = api._get_token()
    dominios_econo = ['econo.unlp.edu.ar','depeco.econo.unlp.edu.ar']
    cantidad_usuarios_econo = 0    
    with open('/tmp/check_mails_google.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['ID','DNI','EMAIL', 'EN GOOGLE', 'ALIAS EN GOOGLE'])
        total = len(uids)
        actual = 0
        logging.info("Cantidad de usuarios a procesar: {}".format(total))        
        for uid in uids:
            actual += 1
            u = users._get_user_uuid(uuid=uid, token=tk)             
            logging.info("Procesando usuario:{} ({}/{})".format(uid, actual, total))
            if u is not None and 'mails' in u:
                mails_econo = [m["email"] for m in u["mails"] if m["confirmado"] and m["eliminado"] is None and len(m["email"].split('@')) > 1 and m["email"].split('@')[1] in dominios_econo]
                if len(mails_econo) > 0:
                    logging.info("El usuario {} posee cuenta instucional".format(u["dni"]))
                    user_google = check_google(u)    
                    cantidad_usuarios_econo +=1                
                    if not user_google:
                        row = [u['id'], u['dni'], ' '.join(mails_econo), 'No', '']
                        writer.writerow(row)
                    else:
                        alias = [m['address'] for m in user_google['emails'] if m['address'].split('@')[0] != u['dni']]
                        row = [u['id'], u['dni'], ' '.join(mails_econo), 'Si', ' '.join(alias)]
                        writer.writerow(row)
    csvFile.close()
    logging.info("Cantidad de usuarios econo procesados: {}".format(cantidad_usuarios_econo))

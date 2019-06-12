
from flask import Blueprint, request
from .converters import ListConverter

bp = Blueprint('gelis', __name__, url_prefix='/gelis/api/v1.0')

permisos = {
    'DESIGNATIONS_READ':'urn:gelis:designations:read',
    'PLACE_CREATE':'urn:gelis:place:create'
}

import os
VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
OIDC_URL = os.environ['OIDC_URL']

client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']

from warden.sdk.warden import Warden
warden_url = os.environ['WARDEN_API_URL']
warden = Warden(OIDC_URL, warden_url, client_id, client_secret, verify=VERIFY_SSL)



def obtener_lista_permisos(permisos):
    return [p for p in permisos.values()]

@bp.before_app_request
def antes_de_cada_requerimiento():
    pass

import os
WARDEN_API_URL = os.environ['WARDEN_API_URL']

@bp.route('/registrar', methods=['GET'])
def registrar_permisos():
    permissions = obtener_lista_permisos(permisos)
    warden.register_system_perms(permisos)
    return ('',200)

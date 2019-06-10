
from flask import Blueprint, request
from .converters import ListConverter

bp = Blueprint('gelis', __name__, url_prefix='/gelis/api/v1.0')

permisos = {
    'DESIGNATIONS_READ':'urn:gelis:designations:read',
    'PLACE_CREATE':'urn:gelis:place:create'
}

def obtener_lista_permisos(permisos):
    return [p for p in permisos.values()]


@bp.before_app_request
def antes_de_cada_requerimiento():
    pass

import os
WARDEN_API_URL = os.environ['WARDEN_API_URL']

@bp.route('/registrar', methods=['GET'])
def designaciones_por_lugares():
    import requests
    data = {
        'system': 'gelis-api',
        'permissions': obtener_lista_permisos(permisos)
    }
    r = requests.post(WARDEN_API_URL + '/registrar_permisos', json=data)
    return r
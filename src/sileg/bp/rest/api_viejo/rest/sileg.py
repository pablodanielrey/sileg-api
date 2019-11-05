import logging
logging.getLogger().setLevel(logging.DEBUG)
import sys
import os
from dateutil import parser

from flask import Flask, abort, make_response, jsonify, url_for, request, json
from flask_jsontools import jsonapi
from dateutil import parser

from flask import Blueprint
from .converters import ListConverter

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
OIDC_URL = os.environ['OIDC_URL']

client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']

from warden.sdk.warden import Warden
warden_url = os.environ['WARDEN_API_URL']
warden = Warden(OIDC_URL, warden_url, client_id, client_secret, verify=VERIFY_SSL)

from rest_utils import register_encoder
from sileg.model.SilegModel import SilegModel
from sileg.model import obtener_session

API_BASE = os.environ['API_BASE']

app = Blueprint('gelis', __name__, url_prefix=API_BASE)


@app.route('/obtener_config', methods=['GET'])
@jsonapi
def retornar_config_ui():
    config = SilegModel._config()
    return config['ui']

@app.route('/acceso_modulos', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_acceso_modulos(token=None):
    config = SilegModel._config()
    perfiles = config['api']['perfiles']
    for perfil in perfiles:
        p = perfil['perfil']
        response = warden.has_all_profiles(token, [p])
        if 'profile' in response and response['profile']:
            return perfil['funciones']
   
    """
        si no matcheo anteriorment entonces retorno un arreglo vacio sin funciones
    """
    return json.dumps([])

"""
    //////////////////////////////////
    métodos usados en la web sileg-ui
    /////////////////////////////////
"""

@app.route('/usuarios/<search>/search', methods=['GET'])
@warden.require_valid_token
@jsonapi
def usuarios_search(search, token=None):
    autorizador_id = token['sub']

    prof = warden.has_one_profile(token, ['gelis-super-admin','gelis-admin','gelis-operator'])
    if prof and prof['profile']:
        with obtener_session() as session:
            usuarios = SilegModel.usuarios_admin_search(session, autorizador_id, search)
            return usuarios
    
    with obtener_session() as session:
        usuarios = SilegModel.usuarios_search(session, autorizador_id, search)
        return usuarios


@app.route('/print_routes', methods=['GET'])
@jsonapi
def print_routes():
    r = [
        url_for('usuarios_search', search=' '),
        url_for('options', path='/usuarios/ /search')
    ]
    return r

"""
    //////////////////////////////
"""



'''
@app.route('/usuarios/<uid>/telefono', methods=['POST'])
@warden.require_valid_token
@jsonapi
def crear_telefono(uid, token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    telefono = request.get_json()
    assert uid is not None
    assert telefono is not None
    return SilegModel.agregarTelefono(uid, telefono)
'''

@app.route('/usuarios/<uid>/lugares', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_lugares_por_usuario(uid=None, token=None):
    assert uid is not None

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if prof and prof['profile']:
        with obtener_session() as session:
            lugares = SilegModel.obtener_lugares_por_usuario(session, uid)
            return lugares

    usuario_logueado = token['sub']
    if usuario_logueado == uid:
        with obtener_session() as session:
            lugares = SilegModel.obtener_lugares_por_usuario(session, uid)
            return lugares

    return ('no tiene los permisos suficientes', 403)


@app.route('/usuarios/<uid>/designaciones', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_designaciones_por_usuario(uid=None, token=None):
    assert uid is not None

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if prof and prof['profile']:
        with obtener_session() as session:
            designaciones = SilegModel.designaciones(session=session, persona=uid, historico=True, expand=True)
            logging.debug(designaciones)
            return designaciones

    usuario_logueado = token['sub']
    with obtener_session() as session:
        if SilegModel.chequear_acceso_designaciones(session, usuario_logueado, uid):
            designaciones = SilegModel.designaciones(session=session, persona=uid, historico=True, expand=True)
            logging.debug(designaciones)
            return designaciones
        else:
            return ('no tiene los permisos suficientes', 403)



@app.route('/usuarios/<uid>/subusuarios', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_subusuarios(uid, token=None):
    """
        obtengo los usuarios que están en la misma oficina o suboficinas del usuario identificado por uid
    """
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if not prof or prof['profile'] == False:
        if uid != token['sub']:
            return ('no tiene los permisos suficientes', 403)

    with obtener_session() as session:
        return SilegModel.obtener_subusuarios_por_usuario(session, uid)



@app.route('/designaciones/', methods=['GET'])
@warden.require_valid_token
@jsonapi
def designaciones(token):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if not prof or not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    lugar = request.args.get('l',None)
    persona = request.args.get('p',None)
    historico = request.args.get('h',False,bool)
    with obtener_session() as session:
        designaciones = SilegModel.designaciones(session,offset=offset, limit=limit, lugar=lugar, persona=persona, historico=historico)
        designaciones.append('cantidad:{}'.format(len(designaciones)))
        return designaciones

"""
@app.route('/designacion', methods=['POST'])
@warden.require_valid_token
@jsonapi
def crearDesignacion(token=None):
    ''' crea una nueva designacion, solo permite crear cumplimiento de funciones '''

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    pedido = request.get_json()
    logging.debug(pedido)
    with obtener_session() as session:
        d = SilegModel.crearDesignacionCumpliendoFuncionesConCorreo(session, pedido)
        session.commit()
        logging.debug(json.dumps(d))
        return d.id
"""


@app.route('/designacion-sin-correo', methods=['PUT'])
@warden.require_valid_token
@jsonapi
def crearDesignacionSinCorreo(token):
    ''' crea una nueva designacion, solo permite crear cumplimiento de funciones '''

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    pedido = request.get_json()
    logging.debug(pedido)
    with obtener_session() as session:
        d = SilegModel.crearDesignacionCumpliendoFunciones(session, pedido)
        session.commit()
        logging.debug(json.dumps(d))
        return d.id

@app.route('/designacion/<did>', methods=['PUT'])
@warden.require_valid_token
@jsonapi
def modificar_designacion(did, token):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    designacion = request.get_json()
    assert did is not None
    assert designacion is not None
    fecha_str = designacion["desde"]
    designacion["desde"] = parser.parse(fecha_str) if fecha_str else None

    with obtener_session() as session:
        SilegModel.actualizarDesignacion(session, did, designacion)
        session.commit()

@app.route('/designacion/<did>', methods=['DELETE'])
@warden.require_valid_token
@jsonapi
def eliminar_designacion(did, token):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert did is not None
    logging.info("Eliminar designacion")
    with obtener_session() as session:
        SilegModel.eliminarDesignacion(session, did)
        session.commit()
        return True

@app.route('/designacion/<did>/detalle', methods=['GET'])
@warden.require_valid_token
@jsonapi
def detalle_designacion(did, token):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert did is not None
    with obtener_session() as session:
        return SilegModel.detalleDesignacion(session, did)

"""
@app.route('/prorrogas/<designacion>', methods=['GET'])
@warden.require_valid_token
@jsonapi
def prorrogas(designacion, token=None):
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    lugar = request.args.get('l',None)
    persona = request.args.get('p',None)
    historico = request.args.get('h',False,bool)
    with obtener_session() as session:
        return SilegModel.prorrogas(session=session, offset=offset, limit=limit, designacion=designacion, lugar=lugar, persona=persona, historico=historico)
"""

@app.route('/cargos', methods=['GET'])
@warden.require_valid_token
@jsonapi
def cargos(token=None):
    with obtener_session() as session:
        return SilegModel.cargos(session)

@app.route('/lugares', methods=['PUT'])
@warden.require_valid_token
@jsonapi
def crearLugar(token=None):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    lugar = request.get_json()
    with obtener_session() as session:
        l = SilegModel.crearLugar(session, lugar)
        session.commit()
        logging.debug(json.dumps(l))
        return l

@app.route('/lugares/<lid>', methods=['POST'])
@warden.require_valid_token
@jsonapi
def modificar_lugar(lid=None, token=None):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)
    lugar = request.get_json()
    with obtener_session() as session:
        SilegModel.modificarLugar(session, lugar)
        session.commit()

@app.route('/lugares/<lid>', methods=['DELETE'])
@warden.require_valid_token
@jsonapi
def eliminar_lugar(lid, token):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)
    assert lid is not None
    with obtener_session() as session:
        fecha = SilegModel.eliminarLugar(session, lid)
        session.commit()
        return fecha

@app.route('/lugares/<lid>/restaurar', methods=['GET'])
@warden.require_valid_token
@jsonapi
def restaurar_lugar(lid, token=None):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)
    assert lid is not None
    with obtener_session() as session:
        id = SilegModel.restaurarLugar(session, lid)
        session.commit()
        return id

@app.route('/lugares/<lid>/designaciones', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_desginaciones_lugar(lid, token=None):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if not prof or not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert lid is not None
    with obtener_session() as session:
        return SilegModel.obtenerDesignacionesLugar(session, lid)


@app.route('/lugares/<lid>/subusuarios', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_lugar_subusuarios(lid, token=None):
    """
        obtengo los usuarios que están en el arbol de las oficinas que tiene como raiz lid
    """
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if not prof or prof['profile'] == False:
        return ('no tiene los permisos suficientes', 403)

    with obtener_session() as session:
        return SilegModel.obtener_subusuarios_por_lugares(session, [lid])

@app.route('/lugares/<lid>/sublugares', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_lugar_sublugares(lid, token=None):
    """
        obtengo los lugares que están en el arbol de las oficinas que tiene como raiz lid
    """
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if not prof or prof['profile'] == False:
        return ('no tiene los permisos suficientes', 403)

    with obtener_session() as session:
        sublugares = SilegModel.obtener_sublugares(session, lid)
        return list(set(sublugares))

@app.route('/lugares/<lid>/arbol', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_lugar_subarbol(lid, token=None):
    """
        obtengo todos los cargos y lugares que cuelgan de lid, retornados en formato de arbol json.
    """
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if not prof or prof['profile'] == False:
        return ('no tiene los permisos suficientes', 403)

    with obtener_session() as session:
        arbol = SilegModel.obtener_arbol(session, lid)
        return arbol



@app.route('/lugares/', methods=['GET'], defaults={'lid':None})
@app.route('/lugares/<lid>', methods=['GET'])
@warden.require_valid_token
@jsonapi
def lugares(lid=None, token=None):
    with obtener_session() as session:
        if lid:
            return SilegModel.lugar(session, lid)
        else:
            search = request.args.get('q')
            lugares = SilegModel.lugares(session=session, search=search)
            catedras = SilegModel.obtener_catedras_por_nombre(session=session, search=search)
            lugares.extend(catedras)
            return lugares

@app.route('/departamentos/', methods=['GET'])
@warden.require_valid_token
@jsonapi
def departamentos(token=None):
    with obtener_session() as session:
        return SilegModel.departamentos(session)

@app.route('/materias/', methods=['GET'], defaults={'materia':None})
@app.route('/materias/<materia>', methods=['GET'])
@warden.require_valid_token
@jsonapi
def materias(materia=None, token=None):
    catedra = request.args.get('c',None)
    departamento = request.args.get('d',None)
    with obtener_session() as session:
        return SilegModel.materias(session=session, materia=materia, catedra=catedra, departamento=departamento)

@app.route('/catedras/', methods=['GET'], defaults={'catedra':None})
@app.route('/catedras/<catedra>', methods=['GET'])
@warden.require_valid_token
@jsonapi
def catedras(catedra=None, token=None):
    materia = request.args.get('m',None)
    departamento = request.args.get('d',None)
    with obtener_session() as session:
        return SilegModel.catedras(session=session, catedra=catedra, materia=materia, departamento=departamento)

import datetime
from functools import reduce

@app.route('/designaciones/pendientes/lugares/<list:ids>', methods=['GET'])
# @warden.require_valid_token
@jsonapi
def desginaciones_pendientes(ids=[], token=None):
    # prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    # if not prof['profile']:
    #     return ('no tiene los permisos suficientes', 403)
    with obtener_session() as session:
        data = []
        aux = []    
        lids = set([ aux + SilegModel.obtener_sublugares(session,id) for id in ids ][0])
        for lid in lids:
            desig_lug = SilegModel.obtenerDesignacionesLugar(session, lid)
            designaciones = []
            for d in desig_lug['designaciones']:
                estado = {'fecha': datetime.date.today(), 'nombre': 'Alta Pendiente', 'authorized': '89d88b81-fbc0-48fa-badb-d32854d3d93a'}
                designaciones.append({'designacion': d['designacion'], 'ptos': 10, 'estado': estado, 'usuario': d['usuario']})
            data.append({'lugar':desig_lug['lugar'], 'designaciones': designaciones, 'ptos_alta': 65, 'ptos_baja': 60})
        return data

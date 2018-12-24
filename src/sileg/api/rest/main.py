import logging
logging.getLogger().setLevel(logging.DEBUG)
import sys
import os
from dateutil import parser

from werkzeug.contrib.fixers import ProxyFix

from flask import Flask, abort, make_response, jsonify, url_for, request, json
from flask_jsontools import jsonapi
from dateutil import parser

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

# set the project root directory as the static folder, you can set others.
from flask_cors import CORS

app = Flask(__name__, static_url_path='/src/sileg/web')
app.wsgi_app = ProxyFix(app.wsgi_app)
register_encoder(app)
CORS(app)

DEBUGGING = bool(int(os.environ.get('VSC_DEBUGGING',0)))
def configurar_debugger():
    """
    para debuggear con visual studio code
    """
    if DEBUGGING:
        print('Iniciando Debugger PTVSD')
        import ptvsd
        #secret = os.environ.get('VSC_DEBUG_KEY',None)
        port = int(os.environ.get('VSC_DEBUGGING_PORT', 5678))
        ptvsd.enable_attach(address=('0.0.0.0',port))

configurar_debugger()


API_BASE = os.environ['API_BASE']

@app.route(API_BASE + '/obtener_config', methods=['GET'])
@jsonapi
def retornar_config_ui():
    config = SilegModel._config()
    return config['ui']

@app.route(API_BASE + '/acceso_modulos', methods=['GET'])
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
    prof = warden.has_one_profile(token, ['gelis-super-admin'])
    if prof and prof['profile'] == True:
        a = [
            'super-admin'
        ]
        return json.dumps(a)

    prof = warden.has_one_profile(token, ['gelis-admin'])
    if prof and prof['profile'] == True:
        a = [
            'buscar_usuario',
            'crear_usuario',
            'buscar_lugar',
            'crear_lugar',
            'sincronizacion_usuario',
            'sincronizacion_login'
        ]
        return json.dumps(a)

    prof = warden.has_one_profile(token, ['gelis-operator'])
    if prof and prof['profile'] == True:
        a = [
            'buscar_usuario',
            'buscar_lugar',
            'sincronizacion_usuario',
            'sincronizacion_login'
        ]
        return json.dumps(a)
    a = []
    return json.dumps(a)
    """

"""
    //////////////////////////////////
    métodos usados en la web sileg-ui
    /////////////////////////////////
"""

@app.route(API_BASE + '/usuarios/<search>/search', methods=['GET'])
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


@app.route(API_BASE + '/print_routes', methods=['GET'])
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
@app.route(API_BASE + '/usuarios/<uid>/telefono', methods=['POST'])
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

@app.route(API_BASE + '/usuarios/<uid>/lugares', methods=['GET'])
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


@app.route(API_BASE + '/usuarios/<uid>/designaciones', methods=['GET'])
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



@app.route(API_BASE + '/usuarios/<uid>/subusuarios', methods=['GET'])
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



@app.route(API_BASE + '/designaciones/', methods=['GET'])
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
@app.route(API_BASE + '/designacion', methods=['POST'])
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


@app.route(API_BASE + '/designacion-sin-correo', methods=['PUT'])
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

@app.route(API_BASE + '/designacion/<did>', methods=['PUT'])
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

@app.route(API_BASE + '/designacion/<did>', methods=['DELETE'])
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

@app.route(API_BASE + '/designacion/<did>/detalle', methods=['GET'])
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
@app.route(API_BASE + '/prorrogas/<designacion>', methods=['GET'])
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

@app.route(API_BASE + '/cargos', methods=['GET'])
@warden.require_valid_token
@jsonapi
def cargos(token=None):
    with obtener_session() as session:
        return SilegModel.cargos(session)

@app.route(API_BASE + '/lugares', methods=['PUT'])
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

@app.route(API_BASE + '/lugares/<lid>', methods=['POST'])
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

@app.route(API_BASE + '/lugares/<lid>', methods=['DELETE'])
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

@app.route(API_BASE + '/lugares/<lid>/restaurar', methods=['GET'])
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

@app.route(API_BASE + '/lugares/<lid>/designaciones', methods=['GET'])
@warden.require_valid_token
@jsonapi
def obtener_desginaciones_lugar(lid, token=None):
    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin', 'gelis-operator'])
    if not prof or not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert lid is not None
    with obtener_session() as session:
        return SilegModel.obtenerDesignacionesLugar(session, lid)


@app.route(API_BASE + '/lugares/<lid>/subusuarios', methods=['GET'])
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

@app.route(API_BASE + '/lugares/<lid>/sublugares', methods=['GET'])
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

@app.route(API_BASE + '/lugares/<lid>/arbol', methods=['GET'])
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



@app.route(API_BASE + '/lugares/', methods=['GET'], defaults={'lid':None})
@app.route(API_BASE + '/lugares/<lid>', methods=['GET'])
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

@app.route(API_BASE + '/departamentos/', methods=['GET'])
@warden.require_valid_token
@jsonapi
def departamentos(token=None):
    with obtener_session() as session:
        return SilegModel.departamentos(session)

@app.route(API_BASE + '/materias/', methods=['GET'], defaults={'materia':None})
@app.route(API_BASE + '/materias/<materia>', methods=['GET'])
@warden.require_valid_token
@jsonapi
def materias(materia=None, token=None):
    catedra = request.args.get('c',None)
    departamento = request.args.get('d',None)
    with obtener_session() as session:
        return SilegModel.materias(session=session, materia=materia, catedra=catedra, departamento=departamento)

@app.route(API_BASE + '/catedras/', methods=['GET'], defaults={'catedra':None})
@app.route(API_BASE + '/catedras/<catedra>', methods=['GET'])
@warden.require_valid_token
@jsonapi
def catedras(catedra=None, token=None):
    materia = request.args.get('m',None)
    departamento = request.args.get('d',None)
    with obtener_session() as session:
        return SilegModel.catedras(session=session, catedra=catedra, materia=materia, departamento=departamento)


"""
@app.route(API_BASE + '<path:path>', methods=['OPTIONS'])
def options():
    if request.method == 'OPTIONS':
        return 204
    return 204

@app.after_request
def cors_after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Allow', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
"""

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'

    return r

def main():
    app.run(host='0.0.0.0', port=10202, debug=False)

if __name__ == '__main__':
    main()

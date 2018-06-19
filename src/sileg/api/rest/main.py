import logging
logging.getLogger().setLevel(logging.DEBUG)
import sys
import os
from dateutil import parser

from werkzeug.contrib.fixers import ProxyFix

from flask import Flask, abort, make_response, jsonify, url_for, request, json
from flask_jsontools import jsonapi
from dateutil import parser

import oidc
from oidc.oidc import TokenIntrospection
client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']
rs = TokenIntrospection(client_id, client_secret)

from warden.sdk.warden import Warden
warden_url = os.environ['WARDEN_API_URL']
warden = Warden(warden_url, client_id, client_secret)

from rest_utils import register_encoder

from sileg.model.SilegModel import SilegModel
from sileg.model import Session

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/src/sileg/web')
app.wsgi_app = ProxyFix(app.wsgi_app)
register_encoder(app)

API_BASE = os.environ['API_BASE']

@app.route(API_BASE + '/usuarios/', methods=['GET'], defaults={'uid':None})
@app.route(API_BASE + '/usuarios/<uid>', methods=['GET'])
@rs.require_valid_token
@jsonapi
def usuarios(uid=None, token=None):
    c = False

    prof = warden.has_all_profiles(token, ['gelis-super-admin'])
    if prof['profile']:
        c = request.args.get('c',False,bool)
    else:
        prof = warden.has_all_profiles(token, ['gelis-admin'])
        if not prof['profile']:
            return ('no tiene los permisos suficientes', 403)


    search = request.args.get('q',None)
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)


    s = Session()
    try:
        r = None
        if uid:
            r = SilegModel.usuario(s, uid, retornarClave=c)
        else:
            fecha_str = request.args.get('f', None)
            fecha = parser.parse(fecha_str) if fecha_str else None
            r = SilegModel.usuarios(session=s, search=search, retornarClave=c, offset=offset, limit=limit, fecha=fecha)
        
        return r

    except Exception as e:
        logging.exception(e)
        raise e

    finally:
        s.close()

@app.route(API_BASE + '/usuarios', methods=['PUT','POST'])
@rs.require_valid_token
@jsonapi
def crear_usuario(token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    usuario = request.get_json()
    if not usuario:
        raise Exception('usuario == None')
    logging.debug(usuario)
    return SilegModel.crearUsuario(usuario)


@app.route(API_BASE + '/usuarios/<uid>', methods=['POST'])
@rs.require_valid_token
@jsonapi
def actualizar_usuario(uid, token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    usuario = request.get_json()
    assert uid is not None
    assert usuario is not None
    return SilegModel.actualizarUsuario(uid, usuario)


@app.route(API_BASE + '/usuarios/<uid>/correos/<cid>', methods=['DELETE'])
@app.route(API_BASE + '/correos/<cid>', methods=['DELETE'])
@rs.require_valid_token
@jsonapi
def eliminar_correo(uid=None, cid=None, token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert cid is not None
    return SilegModel.eliminarCorreo(uid, cid)

@app.route(API_BASE + '/usuarios/<uid>/correos', methods=['PUT','POST'])
@rs.require_valid_token
@jsonapi
def agregar_correo(uid=None, token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    datos = request.get_json()
    logging.debug(datos)
    s = Session()
    try:
        r = SilegModel.agregarCorreo(s, uid, datos['correo'])
        return r

    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/usuarios/<uid>/designaciones', methods=['GET'])
@rs.require_valid_token
@jsonapi
def obtener_designaciones_por_usuario(uid=None, token=None):
    assert uid is not None
    s = Session()
    try:
        designaciones = SilegModel.designaciones(session=s, persona=uid, historico=True, expand=True)
        logging.debug(designaciones)
        return designaciones
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()


@app.route(API_BASE + '/generar_clave/<uid>', methods=['GET'])
@rs.require_valid_token
@jsonapi
def generar_clave(uid, token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert uid is not None
    return SilegModel.generarClave(uid)

@app.route(API_BASE + '/correo/<cuenta>', methods=['GET'])
@rs.require_valid_token
@jsonapi
def verificarDisponibilidadCorreo(cuenta=None, token=None):
    if request.method == 'OPTIONS':
        return 204
    assert cuenta is not None
    assert '@' in cuenta
    return SilegModel.verificarDisponibilidadCorreo(cuenta)

@app.route(API_BASE + '/designaciones/', methods=['GET'])
@rs.require_valid_token
@jsonapi
def designaciones(token):
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    lugar = request.args.get('l',None)
    persona = request.args.get('p',None)
    historico = request.args.get('h',False,bool)
    s = Session()
    try:
        designaciones = SilegModel.designaciones(s,offset=offset, limit=limit, lugar=lugar, persona=persona, historico=historico)
        designaciones.append('cantidad:{}'.format(len(designaciones)))
        return designaciones
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/designacion', methods=['POST'])
@rs.require_valid_token
@jsonapi
def crearDesignacion(token=None):
    ''' crea una nueva designacion, solo permite crear cumplimiento de funciones '''

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    pedido = request.get_json()
    logging.debug(pedido)
    s = Session()
    try:
        d = SilegModel.crearDesignacionCumpliendoFuncionesConCorreo(s, pedido)
        s.commit()
        logging.debug(json.dumps(d))
        return d.id

    except Exception as e:
        s.rollback()
        logging.exception(e)
        raise e

    finally:
        s.close()

@app.route(API_BASE + '/designacion-sin-correo', methods=['PUT'])
@rs.require_valid_token
@jsonapi
def crearDesignacionSinCorreo(token):
    ''' crea una nueva designacion, solo permite crear cumplimiento de funciones '''

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    pedido = request.get_json()
    logging.debug(pedido)
    s = Session()
    try:
        d = SilegModel.crearDesignacionCumpliendoFunciones(s, pedido)
        s.commit()
        logging.debug(json.dumps(d))
        return d.id

    except Exception as e:
        s.rollback()
        logging.exception(e)
        raise e

    finally:
        s.close()

@app.route(API_BASE + '/designacion/<did>', methods=['PUT'])
@rs.require_valid_token
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


    session = Session()
    try:
        SilegModel.actualizarDesignacion(session, did, designacion)
        session.commit()
    finally:
        session.close()

@app.route(API_BASE + '/designacion/<did>', methods=['DELETE'])
@rs.require_valid_token
@jsonapi
def eliminar_designacion(did, token):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert did is not None
    logging.info("Eliminar designacion")
    session = Session()
    try:
        SilegModel.eliminarDesignacion(session, did)
        session.commit()
        return True
    finally:
        session.close()

@app.route(API_BASE + '/prorrogas/<designacion>', methods=['GET'])
@rs.require_valid_token
@jsonapi
def prorrogas(designacion, token=None):
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    lugar = request.args.get('l',None)
    persona = request.args.get('p',None)
    historico = request.args.get('h',False,bool)
    s = Session()
    try:
        return SilegModel.prorrogas(session=s, offset=offset, limit=limit, designacion=designacion, lugar=lugar, persona=persona, historico=historico)
    except Exception as e:
        logging.exception(e)
        raise e

    finally:
        s.close()

@app.route(API_BASE + '/cargos', methods=['GET'])
@rs.require_valid_token
@jsonapi
def cargos(token=None):
    s = Session()
    try:
        return SilegModel.cargos(s)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/lugares', methods=['PUT'])
@rs.require_valid_token
@jsonapi
def crearLugar(token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    lugar = request.get_json()
    s = Session()
    try:
        l = SilegModel.crearLugar(s, lugar)
        s.commit()
        logging.debug(json.dumps(l))
        return l

    except Exception as e:
        s.rollback()
        logging.exception(e)
        raise e

    finally:
        s.close()

@app.route(API_BASE + '/lugares/<lid>', methods=['POST'])
@rs.require_valid_token
@jsonapi
def modificar_lugar(lid=None, token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    lugar = request.get_json()
    session = Session()
    try:
        SilegModel.modificarLugar(session, lugar)
        session.commit()
    finally:
        session.close()

@app.route(API_BASE + '/lugares/<lid>', methods=['DELETE'])
@rs.require_valid_token
@jsonapi
def eliminar_lugar(lid, token):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert lid is not None
    session = Session()
    try:
        fecha = SilegModel.eliminarLugar(session, lid)
        session.commit()
        return fecha
    finally:
        session.close()

@app.route(API_BASE + '/lugares/<lid>/restaurar', methods=['GET'])
@rs.require_valid_token
@jsonapi
def restaurar_lugar(lid, token=None):

    prof = warden.has_one_profile(token, ['gelis-super-admin', 'gelis-admin'])
    if not prof['profile']:
        return ('no tiene los permisos suficientes', 403)

    assert lid is not None
    session = Session()
    try:
        id = SilegModel.restaurarLugar(session, lid)
        session.commit()
        return id

    finally:
        session.close()

@app.route(API_BASE + '/lugares/<lid>/designaciones', methods=['GET'])
@rs.require_valid_token
@jsonapi
def obtener_desginaciones_lugar(lid, token=None):
    assert lid is not None
    session = Session()
    try:
        return SilegModel.obtenerDesignacionesLugar(session, lid)
    finally:
        session.close()


@app.route(API_BASE + '/lugares/', methods=['GET'], defaults={'lid':None})
@app.route(API_BASE + '/lugares/<lid>', methods=['GET'])
@rs.require_valid_token
@jsonapi
def lugares(lid=None, token=None):
    s = Session()
    try:
        if lid:
            return SilegModel.lugar(s, lid)
        else:
            search = request.args.get('q')
            lugares = SilegModel.lugares(session=s, search=search)
            catedras = SilegModel.obtener_catedras_por_nombre(session=s, search=search)
            lugares.extend(catedras)
            return lugares
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/departamentos/', methods=['GET'])
@rs.require_valid_token
@jsonapi
def departamentos(token=None):
    s = Session()
    try:
        return SilegModel.departamentos(s)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/materias/', methods=['GET'], defaults={'materia':None})
@app.route(API_BASE + '/materias/<materia>', methods=['GET'])
@rs.require_valid_token
@jsonapi
def materias(materia=None, token=None):
    catedra = request.args.get('c',None)
    departamento = request.args.get('d',None)
    s = Session()
    try:
        return SilegModel.materias(session=s, materia=materia, catedra=catedra, departamento=departamento)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/catedras/', methods=['GET'], defaults={'catedra':None})
@app.route(API_BASE + '/catedras/<catedra>', methods=['GET'])
@rs.require_valid_token
@jsonapi
def catedras(catedra=None, token=None):
    materia = request.args.get('m',None)
    departamento = request.args.get('d',None)
    s = Session()
    try:
        return SilegModel.catedras(session=s, catedra=catedra, materia=materia, departamento=departamento)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()


@app.route(API_BASE + '*', methods=['OPTIONS'])
def options():
    if request.method == 'OPTIONS':
        return 204
    return 204

@app.after_request
def cors_after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

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
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()

import logging
logging.getLogger().setLevel(logging.DEBUG)
import sys
import os
from dateutil import parser

from werkzeug.contrib.fixers import ProxyFix

from flask import Flask, abort, make_response, jsonify, url_for, request, json
from flask_jsontools import jsonapi
from dateutil import parser

from rest_utils import register_encoder

from sileg.model.SilegModel import SilegModel
from sileg.model import Session

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/src/sileg/web')
app.wsgi_app = ProxyFix(app.wsgi_app)
register_encoder(app)

API_BASE = os.environ['API_BASE']

@app.route(API_BASE + '/usuarios/', methods=['GET', 'OPTIONS'], defaults={'uid':None})
@app.route(API_BASE + '/usuarios/<uid>', methods=['GET', 'OPTIONS'])
@jsonapi
def usuarios(uid=None):
    if request.method == 'OPTIONS':
        return 204
    search = request.args.get('q',None)
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    c = request.args.get('c',False,bool)
    s = Session()
    try:
        r = None
        if uid:
            r = SilegModel.usuario(s, uid, retornarClave=c)
        else:
            fecha_str = request.args.get('f', None)
            fecha = parser.parse(fecha_str) if fecha_str else None
            r = SilegModel.usuarios(session=s, search=search, retornarClave=c, offset=offset, limit=limit, fecha=fecha)
        s.commit()
        return r
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/usuarios', methods=['PUT','POST','OPTIONS'])
@jsonapi
def crear_usuario():
    if request.method == 'OPTIONS':
        return 204
    usuario = request.get_json()
    if not usuario:
        raise Exception('usuario == None')
    logging.debug(usuario)
    return SilegModel.crearUsuario(usuario)


@app.route(API_BASE + '/usuarios/<uid>', methods=['POST','OPTIONS'])
@jsonapi
def actualizar_usuario(uid):
    if request.method == 'OPTIONS':
        return 204
    usuario = request.get_json()
    assert uid is not None
    assert usuario is not None
    return SilegModel.actualizarUsuario(uid, usuario)


@app.route(API_BASE + '/usuarios/<uid>/correos/<cid>', methods=['DELETE','OPTIONS'])
@app.route(API_BASE + '/correos/<cid>', methods=['DELETE','OPTIONS'])
@jsonapi
def eliminar_correo(uid=None, cid=None):
    if request.method == 'OPTIONS':
        return 204
    assert cid is not None
    return SilegModel.eliminarCorreo(uid, cid)

@app.route(API_BASE + '/usuarios/<uid>/correos', methods=['PUT','POST','OPTIONS'])
@jsonapi
def agregar_correo(uid=None):
    if request.method == 'OPTIONS':
        return 204
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

@app.route(API_BASE + '/usuarios/<uid>/designaciones', methods=['GET','OPTIONS'])
@jsonapi
def obtener_designaciones_por_usuario(uid=None):
    if request.method == 'OPTIONS':
        return 204
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


@app.route(API_BASE + '/generar_clave/<uid>', methods=['GET','OPTIONS'])
@jsonapi
def generar_clave(uid):
    if request.method == 'OPTIONS':
        return 204
    assert uid is not None
    return SilegModel.generarClave(uid)

@app.route(API_BASE + '/correo/<cuenta>', methods=['GET','OPTIONS'])
@jsonapi
def verificarDisponibilidadCorreo(cuenta=None):
    if request.method == 'OPTIONS':
        return 204
    assert cuenta is not None
    assert '@' in cuenta
    return SilegModel.verificarDisponibilidadCorreo(cuenta)

@app.route(API_BASE + '/designaciones/', methods=['GET','OPTIONS'])
@jsonapi
def designaciones():
    if request.method == 'OPTIONS':
        return 204
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    lugar = request.args.get('l',None)
    persona = request.args.get('p',None)
    historico = request.args.get('h',False,bool)
    s = Session()
    try:
        designaciones = SilegModel.designaciones(offset=offset, limit=limit, lugar=lugar, persona=persona, historico=historico)
        designaciones.append('cantidad:{}'.format(len(designaciones)))
        return designaciones
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/designacion', methods=['POST','OPTIONS'])
@jsonapi
def crearDesignacion():
    if request.method == 'OPTIONS':
        return 204
    ''' crea una nueva designacion, solo permite crear cumplimiento de funciones '''
    pedido = request.get_json();
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


@app.route(API_BASE + '/prorrogas/<designacion>', methods=['GET','OPTIONS'])
@jsonapi
def prorrogas(designacion):
    if request.method == 'OPTIONS':
        return 204
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

@app.route(API_BASE + '/cargos/', methods=['GET','OPTIONS'])
@jsonapi
def cargos():
    if request.method == 'OPTIONS':
        return 204
    s = Session()
    try:
        return SilegModel.cargos(s)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()


@app.route(API_BASE + '/lugares/', methods=['GET','OPTIONS'])
@jsonapi
def lugares():
    if request.method == 'OPTIONS':
        return 204
    s = Session()
    try:
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

@app.route(API_BASE + '/departamentos/', methods=['GET', 'OPTIONS'])
@jsonapi
def departamentos():
    if request.method == 'OPTIONS':
        return 204
    s = Session()
    try:
        return SilegModel.departamentos(s)
    except Exception as e:
        logging.exception(e)
        raise e
    finally:
        s.close()

@app.route(API_BASE + '/materias/', methods=['GET', 'OPTIONS'], defaults={'materia':None})
@app.route(API_BASE + '/materias/<materia>', methods=['GET', 'OPTIONS'])
@jsonapi
def materias(materia=None):
    if request.method == 'OPTIONS':
        return 204
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

@app.route(API_BASE + '/catedras/', methods=['GET', 'OPTIONS'], defaults={'catedra':None})
@app.route(API_BASE + '/catedras/<catedra>', methods=['GET', 'OPTIONS'])
@jsonapi
def catedras(catedra=None):
    if request.method == 'OPTIONS':
        return 204
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

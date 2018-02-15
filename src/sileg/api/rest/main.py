import logging
logging.getLogger().setLevel(logging.DEBUG)
import sys
import os
from dateutil import parser

from flask import Flask, abort, make_response, jsonify, url_for, request, json
from sileg.model.SilegModel import SilegModel
from flask_jsontools import jsonapi
from dateutil import parser

from rest_utils import register_encoder


# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/src/sileg/web')
register_encoder(app)

API_BASE = os.environ['API_BASE']

@app.route(API_BASE + '/usuarios/', methods=['GET', 'POST', 'OPTIONS'], defaults={'uid':None})
@app.route(API_BASE + '/usuarios/<uid>', methods=['GET', 'POST', 'OPTIONS'])
@jsonapi
def usuarios(uid=None):
    search = request.args.get('q',None)
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    c = request.args.get('c',False,bool)
    if uid:
        return SilegModel.usuario(uid, retornarClave=c)
    else:
        fecha_str = request.args.get('f', None)
        fecha = parser.parse(fecha_str) if fecha_str else None
        return SilegModel.usuarios(search=search, retornarClave=c, offset=offset, limit=limit, fecha=fecha)

@app.route(API_BASE + '/designaciones/', methods=['GET', 'POST'])
@jsonapi
def designaciones():
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    lugar = request.args.get('l',None)
    persona = request.args.get('p',None)
    historico = request.args.get('h',False,bool)
    designaciones = SilegModel.designaciones(offset=offset, limit=limit, lugar=lugar, persona=persona, historico=historico)
    designaciones.append('cantidad:{}'.format(len(designaciones)))
    return designaciones

@app.route(API_BASE + '/prorrogas/<designacion>', methods=['GET', 'POST'])
@jsonapi
def prorrogas(designacion):
    offset = request.args.get('offset',None,int)
    limit = request.args.get('limit',None,int)
    lugar = request.args.get('l',None)
    persona = request.args.get('p',None)
    historico = request.args.get('h',False,bool)
    return SilegModel.prorrogas(offset=offset, limit=limit, designacion=designacion, lugar=lugar, persona=persona, historico=historico)

@app.route(API_BASE + '/cargos/', methods=['GET', 'POST'])
@jsonapi
def cargos():
    return SilegModel.cargos()

@app.route(API_BASE + '/lugares/', methods=['GET'])
@jsonapi
def lugares():
    return SilegModel.lugares()

@app.route(API_BASE + '/departamentos/', methods=['GET', 'POST'])
@jsonapi
def departamentos():
    return SilegModel.departamentos()

@app.route(API_BASE + '/materias/', methods=['GET', 'POST'], defaults={'materia':None})
@app.route(API_BASE + '/materias/<materia>', methods=['GET', 'POST'])
@jsonapi
def materias(materia=None):
    catedra = request.args.get('c',None)
    departamento = request.args.get('d',None)
    return SilegModel.materias(materia=materia, catedra=catedra, departamento=departamento)

@app.route(API_BASE + '/catedras/', methods=['GET', 'POST'], defaults={'catedra':None})
@app.route(API_BASE + '/catedras/<catedra>', methods=['GET', 'POST'])
@jsonapi
def catedras(catedra=None):
    materia = request.args.get('m',None)
    departamento = request.args.get('d',None)
    return SilegModel.catedras(catedra=catedra, materia=materia, departamento=departamento)

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

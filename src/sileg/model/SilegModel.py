from sqlalchemy import or_,and_, func
from sqlalchemy.orm import joinedload, with_polymorphic, selectin_polymorphic
import datetime
import requests
import os
import logging
import uuid

from .API import API
from .UserCache import UserCache
from .entities import *

USUARIOS_URL = os.environ['USERS_API_URL']
api = API()

"""
    /////////// los getters de la cache //////////
"""

def _get_user_uuid(uuid, token=None):
    query = '{}/usuarios/{}'.format(USUARIOS_URL, uuid)
    r = api.get(query, token=token)
    if not r.ok:
        return None
    usr = r.json()        
    return usr

def _get_user_dni(dni, token=None):
    query = '{}/usuarios/'.format(USUARIOS_URL)
    r = api.get(query, params={'q':dni}, token=token)
    if not r.ok:
        return None
    for usr in r.json():
        return usr        
    return None

"""
    ////////////////
"""


class SilegModel:

    
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

    cache = UserCache(REDIS_HOST, REDIS_PORT, _get_user_uuid, _get_user_dni)


    @staticmethod
    def _chequearParam(param, d):
        assert param in d
        assert d[param] is not None

    @classmethod
    def crearDesignacionCumpliendoFunciones(cls, session, pedido):
        cls._chequearParam('usuario_id', pedido)
        cls._chequearParam('lugar_id', pedido)

        uid = pedido['usuario_id']

        ''' genero la designacion con los datos pasados '''
        cf = CumpleFunciones()

        d = Designacion()
        d.id = str(uuid.uuid4())
        d.tipo = 'original'
        d.desde = datetime.datetime.now()
        d.usuario_id = uid
        d.cargo_id = cf.id
        d.lugar_id = pedido['lugar_id']
        session.add(d)
        return d
  
    @classmethod
    def _agregar_filtros_comunes(cls, q, persona=None, lugar=None, offset=None, limit=None):
        q = q.filter(Designacion.usuario_id == persona) if persona else q
        q = q.filter(Designacion.lugar_id == lugar) if lugar else q
        q = q.offset(offset) if offset else q
        q = q.limit(limit) if limit else q
        return q

    @classmethod
    def chequear_acceso_designaciones(cls, session, usuario_logueado, uid):
        assert usuario_logueado is not None
        assert uid is not None

        ''' ahora chequeamos que el usuario logueado tenga permisos para consultar las designaciones de uid '''

        return usuario_logueado == uid


    @classmethod
    def designaciones(cls,
                    session,
                    offset=None, limit=None,
                    persona=None,
                    lugar=None,
                    historico=False, expand=False):

        q = Designacion.find(session)
        if not historico:
            q = q.filter(or_(Designacion.historico == None, Designacion.historico == False))

        q = q.order_by(Designacion.desde.desc())
        q = cls._agregar_filtros_comunes(q, offset=offset, limit=limit, persona=persona, lugar=lugar)
        if expand:
            if not lugar:
                q = q.options(joinedload('lugar').joinedload('padre'))
            q = q.options(joinedload('cargo'))
        return q.all()


    @classmethod
    def cargos(cls, session):
        cargos = with_polymorphic(Cargo,[
            Docente,
            CumpleFunciones,
            NoDocente
        ])
        return session.query(cargos).all()


    @classmethod
    def obtener_catedras_por_nombre(cls, session, search=None):
        q = None
        if not search:
            q = session.query(Catedra)
        else:
            q2 = session.query(Materia.id).filter(Materia.nombre.op('~*')(search))
            q = session.query(Catedra).filter(or_(Catedra.materia_id.in_(q2), Catedra.nombre.op('~*')(search)))
        return q.options(joinedload('materia')).all()


    @classmethod
    def lugares(cls, session, search=None):
        lugares = with_polymorphic(Lugar,[
            Direccion,
            Escuela,
            LugarDictado,
            Secretaria,
            Instituto,
            Prosecretaria,
            Maestria,
            Catedra
        ])

        q = None
        if not search:
            q = session.query(lugares)
        else:
            ''' TODO: no se como sacar la subclase Catedra de la consulta. analizar otras posibilidades. ahora esta filtrado '''
            q = session.query(lugares).filter(lugares.Catedra.id == None, lugares.nombre.op('~*')(search))
        return q.all()

    @classmethod
    def lugar(cls, session, lid):

        query = session.query(Lugar).options(
            selectin_polymorphic(Lugar, [Direccion,Escuela,LugarDictado,Secretaria,Instituto,Prosecretaria,Maestria,Catedra]),
            joinedload(Catedra.materia)
        )
        return query.filter(Lugar.id == lid).one_or_none()


    @classmethod
    def departamentos(cls, session):
        return Departamento.find(session).all()

    @classmethod
    def materias(cls, session, materia=None, catedra=None, departamento=None):
        q = Materia.find(session)
        q = q.filter(Materia.id == materia) if materia else q
        q = q.join(Catedra).filter(Catedra.id == catedra) if catedra else q
        q = q.join(Catedra).filter(Catedra.padre_id == departamento) if departamento else q
        return q.all()

    @classmethod
    def catedras(cls, session, catedra=None, materia=None, departamento=None):
        q = Catedra.find(session)
        q = q.filter(Catedra.id == catedra) if catedra else q
        q = q.filter(Catedra.materia_id == materia) if materia else q
        q = q.filter(Catedra.padre_id == departamento) if departamento else q
        return q.options(joinedload('materia'), joinedload('padre')).all()

    @classmethod
    def crearLugar(cls, session, lugar):
        cls._chequearParam('nombre', lugar)
        cls._chequearParam('tipo', lugar)

        # verifico que no exista el lugar
        lugares = with_polymorphic(Lugar,[
            Direccion,
            Escuela,
            LugarDictado,
            Secretaria,
            Instituto,
            Prosecretaria,
            Maestria,
            Catedra
        ])
        nombre = lugar["nombre"].strip()
        l = Lugar(nombre)
        l.id = str(uuid.uuid4())
        l.tipo = lugar["tipo"]

        if "descripcion" in lugar and lugar["descripcion"] is not None:
            l.descripcion = lugar["descripcion"]
        else:
            l.descripcion = ''
        if "numero" in lugar and lugar["numero"] is not None:
            l.numero = lugar["numero"]
        else:
            l.numero = ''
        if "telefono" in lugar and lugar["telefono"] is not None:
            l.telefono = lugar["telefono"]
        else:
            l.telefono = ''
        if "email" in lugar and lugar["email"] is not None:
            l.correo = lugar["email"]
        else:
            l.correo = ''
        session.add(l)
        return l

    @classmethod
    def modificarLugar(cls, session, lugar):
        cls._chequearParam('nombre', lugar)
        cls._chequearParam('tipo', lugar)
        cls._chequearParam('id', lugar)

        # verifico que no exista el lugar
        lugares = with_polymorphic(Lugar,[
            Direccion,
            Escuela,
            LugarDictado,
            Secretaria,
            Instituto,
            Prosecretaria,
            Maestria,
            Catedra
        ])

        l = session.query(lugares).filter(lugares.id == lugar["id"]).one_or_none()
        if l is None:
            raise Exception("Error, no existe el lugar")

        l.nombre = lugar["nombre"].strip()
        l.descripcion = lugar["descripcion"]
        l.tipo = lugar["tipo"]
        l.numero = lugar["numero"]
        l.telefono = lugar["telefono"]
        l.correo = lugar["correo"]

    @classmethod
    def eliminarLugar(cls, session, lid):
        lugares = with_polymorphic(Lugar,[
            Direccion,
            Escuela,
            LugarDictado,
            Secretaria,
            Instituto,
            Prosecretaria,
            Maestria,
            Catedra
        ])

        l = session.query(lugares).filter(lugares.id == lid).one()
        l.eliminado = datetime.datetime.now()
        return l.eliminado

    @classmethod
    def restaurarLugar(cls, session, lid):
        lugares = with_polymorphic(Lugar,[
            Direccion,
            Escuela,
            LugarDictado,
            Secretaria,
            Instituto,
            Prosecretaria,
            Maestria,
            Catedra
        ])

        l = session.query(lugares).filter(lugares.id == lid).one()
        l.eliminado = None
        return l.id

    @classmethod
    def obtenerDesignacionesLugar(cls, session, lid):
        # obtengo el lugares
        lugar = cls.lugar(session, lid)
        # obtengo las designaciones del lugar
        designaciones = []
        desig = cls.designaciones(session=session, lugar=lid)
        tk = api._get_token()
        for d in desig:
            usr = cls.cache.obtener_usuario_por_uid(d.usuario_id, token=tk)
            designaciones.append({'designacion':d, 'usuario': usr})


        return { 'lugar':lugar, 'designaciones': designaciones }


    @classmethod
    def eliminarDesignacion(cls, session, id):
        l = session.query(Designacion).filter(Designacion.id == id).one()
        l.historico = True

    @classmethod
    def actualizarDesignacion(cls, session, id, designacion):
        d = session.query(Designacion).filter(Designacion.id == id).one_or_none()
        if d is None:
            raise Exception("Error, no existe la designación")

        d.desde = designacion["desde"]
        d.cargo_id = designacion["cargo_id"]

from sqlalchemy import or_,and_, func
from sqlalchemy.orm import joinedload, with_polymorphic, selectin_polymorphic
import datetime
import requests
import os
import logging
import uuid

import oidc
from oidc.oidc import ClientCredentialsGrant

from .entities import *


class SilegModel:

    verify = bool(int(os.environ.get('VERIFY_SSL',0)))
    usuarios_url = os.environ['USERS_API_URL']
    client_id = os.environ['OIDC_CLIENT_ID']
    client_secret = os.environ['OIDC_CLIENT_SECRET']

    @classmethod
    def _get_token(cls):
        ''' obtengo un token mediante el flujo client_credentials para poder llamar a la api de usuarios '''
        grant = ClientCredentialsGrant(cls.client_id, cls.client_secret, verify=cls.verify)
        token = grant.get_token(grant.access_token())
        if not token:
            raise Exception()
        return token

    @classmethod
    def api(cls, api, params=None, token=None):
        if not token:
            token = cls._get_token()

        ''' se deben cheqeuar intentos de login, y disparar : SeguridadError en el caso de que se haya alcanzado el máximo de intentos '''
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        logging.debug(api)
        logging.debug(params)
        r = requests.get(api, verify=cls.verify, headers=headers, params=params)
        logging.debug(r)
        return r

    @classmethod
    def api_post(cls, api, data=None, token=None):
        if not token:
            token = cls._get_token()

        ''' se deben cheqeuar intentos de login, y disparar : SeguridadError en el caso de que se haya alcanzado el máximo de intentos '''
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        logging.debug(api)
        logging.debug(data)
        r = requests.post(api, verify=cls.verify, headers=headers, json=data)
        logging.debug(r)
        return r

    @classmethod
    def api_put(cls, api, data=None, token=None):
        if not token:
            token = cls._get_token()

        ''' se deben cheqeuar intentos de login, y disparar : SeguridadError en el caso de que se haya alcanzado el máximo de intentos '''
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        logging.debug(api)
        logging.debug(data)
        r = requests.put(api, verify=cls.verify, headers=headers, json=data)
        logging.debug(r)
        return r

    @classmethod
    def api_delete(cls, api, token=None):
        if not token:
            token = cls._get_token()

        ''' se deben cheqeuar intentos de login, y disparar : SeguridadError en el caso de que se haya alcanzado el máximo de intentos '''
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        logging.debug(api)
        r = requests.delete(api, verify=cls.verify, headers=headers)
        logging.debug(r)
        return r


    @classmethod
    def generarClave(cls, uid):
        query = cls.usuarios_url + '/generar_clave/' + uid
        r = cls.api(query)
        logging.info(r.json())
        return r.json()

    @classmethod
    def _agregarCorreo(cls, session, uid, correo):
        ''' chequeo que la clave del usuario tenga mas de 8 caracteres '''
        datos = cls.usuario(session, uid, retornarClave=True)
        assert 'claves' in datos['usuario']
        assert datos['usuario']['claves'] is not None
        for c in datos['usuario']['claves']:
            if len(c['clave']) >= 8:
                break
        else:
            raise Exception('La clave no cumple los requisitos mínimos')

        logging.debug('tiene designacion asi que se llama a la api de usuarios')
        query = cls.usuarios_url + '/usuarios/{}/correo'.format(uid)
        r = cls.api_post(query, data={'correo':correo})
        if not r.ok:
            raise Exception(r.text)
        logging.info(r.json())
        return r.json()

    @staticmethod
    def _chequearParam(param, d):
        assert param in d
        assert d[param] is not None

    @classmethod
    def crearDesignacionCumpliendoFuncionesConCorreo(cls, session, pedido):
        cls._chequearParam('correo', pedido)
        uid = pedido['usuario_id']
        correo = pedido['correo']
        cls._agregarCorreo(session, uid, correo)
        return cls.crearDesignacionCumpliendoFunciones(session, pedido)

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
    def verificarDisponibilidadCorreo(cls, cuenta):
        query = cls.usuarios_url + '/correo/' + cuenta
        r = cls.api(query)
        if not r.ok:
            raise Exception(r.text)
        logging.info(r.json())
        return r.json()

    @classmethod
    def agregarCorreo(cls, session, uid, correo):
        ''' verifico que tenga designacion '''
        if session.query(Designacion).filter(Designacion.usuario_id == uid).count() <= 0:
            raise Exception('no tiene designacion')
        return cls._agregarCorreo(session, uid, correo)

    @classmethod
    def eliminarCorreo(cls, uid, cid):
        query = cls.usuarios_url + '/usuarios/{}/correos/{}'.format(uid, cid)
        r = cls.api_delete(query)
        if not r.ok:
            raise Exception(r.text)
        logging.info(r.json())
        return r.json()

    @classmethod
    def eliminarTelefono(cls, uid, tid):
        query = cls.usuarios_url + '/usuarios/{}/telefonos/{}'.format(uid, tid)
        r = cls.api_delete(query)
        if not r.ok:
            raise Exception(r.text)
        logging.info(r.json())
        return r.json()

    @classmethod
    def crearUsuario(cls, usuario):
        query = cls.usuarios_url + '/usuarios'
        r = cls.api_put(query, data=usuario)
        if not r.ok:
            raise Exception(r.text)
        logging.info(r.json())
        return r.json()

    @classmethod
    def actualizarUsuario(cls, uid, usuario):
        query = cls.usuarios_url + '/usuarios/{}'.format(uid)
        r = cls.api_post(query, data=usuario)
        if not r.ok:
            raise Exception(r.text)
        logging.info(r.json())
        return r.json()

    '''
    @classmethod
    def agregarTelefono(cls, uid, telefono):
        query = cls.usuarios_url + '/usuarios/{}/telefono'.format(uid)
        r = cls.api_post(query, data=telefono)
        if not r.ok:
            raise Exception(r.text)
        logging.info(r.json())
        return r.json()
    '''

    @classmethod
    def usuario(cls, session, uid, retornarClave=False):
        query = cls.usuarios_url + '/usuarios/' + uid
        query = query + '?c=True' if retornarClave else query
        r = cls.api(query)
        if not r.ok:
            return []
        usr = r.json()
        return {
            'usuario': usr
        }


    @classmethod
    def usuarios(cls, session, search=None, retornarClave=False, fecha=None, offset=None, limit=None):
        logging.debug(fecha)
        query = cls.usuarios_url + '/usuarios/'
        params = {}
        if search:
            params['q'] = search
        if offset:
            params['offset'] = offset
        if limit:
            params['limit'] = limit
        if fecha:
            params['f'] = fecha
        if retornarClave:
            params['c'] = True

        logging.debug(query)
        r = cls.api(query, params)
        if not r.ok:
            return []

        usrs = r.json()
        rusers = [ 
            {
            'usuario': u,
            'sileg': None
            } 
            for u in usrs ]
        return rusers

    @classmethod
    def _agregar_filtros_comunes(cls, q, persona=None, lugar=None, offset=None, limit=None):
        q = q.filter(Designacion.usuario_id == persona) if persona else q
        q = q.filter(Designacion.lugar_id == lugar) if lugar else q
        q = q.offset(offset) if offset else q
        q = q.limit(limit) if limit else q
        return q

    """
    @classmethod
    def prorrogas(cls, session, designacion,
                    persona=None,
                    lugar=None,
                    historico=False,
                    offset=None, limit=None):

        q = Designacion.find(session)
        q = q.filter(Designacion.designacion_id == designacion, Designacion.tipo == 'prorroga')

        if not historico:
            ahora = datetime.datetime.now().date()
            q = q.filter(or_(Designacion.hasta == None, Designacion.hasta >= ahora))

        q = cls._agregar_filtros_comunes(q, persona, lugar, offset, limit)
        q = q.options(joinedload('usuario'), joinedload('lugar'), joinedload('cargo'))
        q = q.order_by(Designacion.desde.desc())
        return q.all()
    """

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
        q = q.filter(Designacion.designacion_id == None, or_(Designacion.tipo == 'original', Designacion.tipo == None))

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
        for d in desig:
            query = cls.usuarios_url + '/usuarios/' + d.usuario_id
            r = cls.api(query)
            usr = r.json() if r.ok else None
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

import psycopg2
from psycopg2.extras import DictCursor
import os
import uuid
import datetime
from sileg.model.entities import Designacion, CategoriaDesignacion, Lugar, Cargo
from sileg.model import obtener_session
from model_utils.API import API
from model_utils.UserCache import UserCache
from model_utils.UsersAPI import UsersAPI

import logging
logging.getLogger().setLevel(logging.DEBUG)

tipo_designacion = ['original', 'baja', 'prorroga', 'extension', 'prorroga de extension']

USERS_API = os.environ['USERS_API_URL']
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
OIDC_URL = os.environ['OIDC_URL']
OIDC_CLIENT_ID = os.environ['OIDC_CLIENT_ID']
OIDC_CLIENT_SECRET = os.environ['OIDC_CLIENT_SECRET']
VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))

_API = API(url=OIDC_URL, 
              client_id=OIDC_CLIENT_ID, 
              client_secret=OIDC_CLIENT_SECRET, 
              verify_ssl=VERIFY_SSL)

_USERS_API = UsersAPI(api_url=USERS_API, api=_API)


api = _API

def _get_user_uuid(uuid, token=None):
    query = '{}/usuarios/{}'.format(USERS_API, uuid)
    r = api.get(query, token=token)
    if not r.ok:
        return None
    usr = r.json()        
    return usr

def _get_user_dni(dni, token=None):
    query = '{}/usuarios/'.format(USERS_API)
    r = api.get(query, params={'q':dni}, token=token)
    if not r.ok:
        return None
    logging.info(r.json())
    for usr in r.json():
        logging.info("USR:::")
        logging.info(usr)
        return usr        
    return None

cache_usuarios = UserCache(host=REDIS_HOST, 
                            port=REDIS_PORT, 
                            user_getter=_USERS_API._get_user_uuid,
                            users_getter=_USERS_API._get_users_uuid,
                            user_getter_dni=_get_user_dni)

def obtener_persona(cur, empleado_id):
    cur.execute("select pers_nrodoc from persona p inner join empleado e on p.pers_id = e.empleado_pers_id where empleado_id = %s",(empleado_id,))
    r = cur.fetchone()
    dni = str(r[0]) if r else None
    tk = api._get_token()
    logging.info("dni:{}".format(dni))
    usr = cache_usuarios.obtener_usuario_por_dni(dni, tk)
    logging.info("Id de la persona con dni {}: {}".format(dni,usr["id"]))
    return usr['id']

def obtener_lugar(session, catxmat_id, lugdetrab):
    old_id = 'lugar{}'.format(lugdetrab) if lugdetrab else str(catxmat_id)
    lugar = session.query(Lugar).filter(Lugar.old_id == old_id).one_or_none()
    return lugar.id if lugar else None

def obtener_cargo(session, cargo_id, dedicacion_id):
    old_id = 'c{}d{}'.format(cargo_id, dedicacion_id)
    cargo = session.query(Cargo).filter(Cargo.old_id == old_id).one_or_none()
    logging.info("OLD ID: {}".format(old_id))
    return cargo.id if cargo else None    

def crear_designacion(session=None,desde=None, hasta=None, old_id=None, historico=False, tipo=tipo_designacion[0], designacion_relacionada=None, resolucion_id=None,
                    observaciones='', categoria=None, expediente=None, resolucion=None, corresponde=None, usuario_id=None, lugar_id=None, cargo_id=None):
    d = session.query(Designacion).filter(Designacion.old_id == old_id).one_or_none()
    if d is None:
        d = Designacion()        
        d.old_id = old_id
        
    d.desde = desde
    d.hasta = hasta
    d.historico = historico
    d.tipo = tipo
    d.observaciones = observaciones
    d.designacion_id = designacion_relacionada
    d.expediente = expediente
    d.resolucion = resolucion
    d.corresponde = corresponde
    d.categorias = [categoria] if categoria else []
    d.usuario_id = usuario_id
    d.lugar_id = lugar_id
    d.cargo_id = cargo_id
    if not d.id:
        d.id = str(uuid.uuid4())
        session.add(d)
    return d

def obtener_prorroga(prorroga_id, cur):
    logging.info("Obtener prorroga id: {}".format(prorroga_id))
    cur.execute("""
        SELECT *
        FROM prorroga
        WHERE prorroga_id = %s
        ORDER BY prorroga_fecha_desde
    """,(prorroga_id,))
    return cur.fetchone()

def obtener_prorrogas_de(prorroga_id, cur):
    prorrogas = []
    p = obtener_prorroga(prorroga_id, cur)
    while p is not None:
        prorrogas.append(p)
        if p['prorroga_prorrogada_con']:
            p = obtener_prorroga(p['prorroga_prorrogada_con'], cur)
        else:
            p = None
    return prorrogas

def obtener_extensiones(desig_id, cur):
    cur.execute(" SELECT * FROM extension WHERE extension_designacion_id = %s",(desig_id,))
    return cur.fetchall()

def obtener_resolucion(cur, resolucion_id):
    cur.execute("select resolucion_numero, resolucion_expediente, resolucion_corresponde from resolucion where resolucion_id = %s",(resolucion_id,))
    r = cur.fetchone()    
    return r if (r["resolucion_numero"] and r["resolucion_numero"] != '') or (r["resolucion_expediente"] and r["resolucion_expediente"] != '') else None

def importar_designacion(d, cur, session):
    logging.info("Importando designacion: {}".format(d))
    id = d["desig_id"]
    old_id = "desig_{}".format(id)
    resolucion = obtener_resolucion(cur=cur, resolucion_id=d["desig_resolucionalta_id"])
    expediente = resolucion["resolucion_expediente"] if resolucion else None
    resol = resolucion["resolucion_numero"] if resolucion else None
    corresponde = resolucion["resolucion_corresponde"] if resolucion else None
    usuario_id = obtener_persona(cur=cur, empleado_id=d["desig_empleado_id"])
    lugar_id = obtener_lugar(session, d["desig_catxmat_id"], d["desig_lugdetrab_id"])
    cargo_id = obtener_cargo(session, d["desig_tipocargo_id"], d["desig_tipodedicacion_id"])   
    desig = crear_designacion(session=session, desde=d["desig_fecha_desde"], hasta=d["desig_fecha_hasta"], old_id=old_id, historico=False, tipo=tipo_designacion[0], designacion_relacionada=None, resolucion_id=d["desig_resolucionalta_id"],
                        observaciones=d["desig_observaciones"], expediente=expediente, resolucion=resol, corresponde=corresponde, usuario_id=usuario_id, lugar_id=lugar_id, cargo_id=cargo_id)

    logging.info("Desginacion creada: {}".format(desig.__dict__))    
    session.commit()
    if d["desig_resolucionbaja_id"]:
        resolucion = obtener_resolucion(cur=cur, resolucion_id=d["desig_resolucionbaja_id"])
        if resolucion:
            logging.info("Crear baja: {}".format(d))      
            expediente = resolucion["resolucion_expediente"] if resolucion else None
            resol = resolucion["resolucion_numero"] if resolucion else None      
            corresponde = resolucion["resolucion_corresponde"] if resolucion else None        
            old_id = "baja_{}".format(id)
            categoria = None 
            if d["desig_tipobaja_id"]:
                categoria = session.query(CategoriaDesignacion).filter(CategoriaDesignacion.old_id == str(d["desig_tipobaja_id"])).one_or_none()
            crear_designacion(session=session, desde=d["desig_fecha_baja"], hasta=None, old_id=old_id, historico=True, tipo=tipo_designacion[1], designacion_relacionada=desig.id, resolucion_id=d["desig_resolucionbaja_id"],
                            observaciones=d["desig_observaciones"], categoria=categoria, expediente=expediente, resolucion=resol, corresponde=corresponde, usuario_id=usuario_id, lugar_id=lugar_id, cargo_id=cargo_id)
            desig.historico = True

    prorrogas = []
    if d["desig_prorrogada_con"]:
        prorrogas = obtener_prorrogas_de(d["desig_prorrogada_con"], cur)
        desig.historico = True
        for p in prorrogas:
            historico = p["prorroga_prorrogada_con"] is None or p["prorroga_resolucionbaja_id"] is not None
            old_id = "prorroga_{}".format(p["prorroga_id"])
            resolucion = obtener_resolucion(cur=cur, resolucion_id=p["prorroga_resolucionalta_id"])            
            expediente = resolucion["resolucion_expediente"] if resolucion else None
            resol = resolucion["resolucion_numero"] if resolucion else None      
            corresponde = resolucion["resolucion_corresponde"] if resolucion else None               
            pro_desig = crear_designacion(session=session,desde=p["prorroga_fecha_desde"], hasta=p["prorroga_fecha_hasta"], old_id=old_id, historico=historico, tipo=tipo_designacion[2],designacion_relacionada=desig.id,
                              resolucion_id=p["prorroga_resolucionalta_id"], observaciones="", expediente=expediente, resolucion=resol, corresponde=corresponde, usuario_id=usuario_id, lugar_id=lugar_id, cargo_id=cargo_id)
            logging.info("Crear prorroga: {}".format(p))
            session.commit()
            # verifico si tiene una baja
            if p["prorroga_resolucionbaja_id"]:
                resolucion = obtener_resolucion(cur=cur, resolucion_id=p["prorroga_resolucionbaja_id"])
                if resolucion:          
                    expediente = resolucion["resolucion_expediente"] if resolucion else None
                    resol = resolucion["resolucion_numero"] if resolucion else None      
                    corresponde = resolucion["resolucion_corresponde"] if resolucion else None                                   
                    old_id = "baja_{}".format(p["prorroga_id"])
                    # si tiene baja creo la designacion baja y la relaciono con la prorroga
                    desde = p["prorroga_fecha_baja"] if p["prorroga_fecha_baja"] else p["prorroga_fecha_hasta"]
                    categoria = None 
                    if p["prorroga_tipobaja_id"]:
                        categoria = session.query(CategoriaDesignacion).filter(CategoriaDesignacion.old_id == str(p["prorroga_tipobaja_id"])).one_or_none()
                    crear_designacion(session=session, desde=desde, hasta=None, old_id=old_id, historico=False, tipo=tipo_designacion[1],designacion_relacionada=pro_desig.id, resolucion_id=p["prorroga_resolucionbaja_id"],
                            observaciones="", categoria=categoria, expediente=expediente, resolucion=resol, corresponde=corresponde, usuario_id=usuario_id, lugar_id=lugar_id, cargo_id=cargo_id)
                    pro_desig.historico = True
    session.commit()        

    extensiones = obtener_extensiones(id, cur)
    for e in extensiones:
        # crear extension
        resolucion = obtener_resolucion(cur=cur, resolucion_id=e["extension_resolucionalta_id"])
        expediente = resolucion["resolucion_expediente"] if resolucion else None
        resol = resolucion["resolucion_numero"] if resolucion else None      
        corresponde = resolucion["resolucion_corresponde"] if resolucion else None                       
        old_id = "extension_{}".format(e["extension_id"])        
        cargo_id = obtener_cargo(session, d["desig_tipocargo_id"], e["extension_nuevadedicacion_id"])   
        ext = crear_designacion(session=session, desde=e["extension_fecha_desde"], hasta=e["extension_fecha_hasta"], old_id=old_id, historico=False, tipo=tipo_designacion[3],designacion_relacionada=desig.id,
                resolucion_id=e["extension_resolucionalta_id"], observaciones="", expediente=expediente, resolucion=resol, corresponde=corresponde, usuario_id=usuario_id, lugar_id=lugar_id, cargo_id=cargo_id)
        session.commit()
        # verifico si tiene baja
        if e["extension_resolucionbaja_id"]:
            resolucion = obtener_resolucion(cur=cur, resolucion_id=e["extension_resolucionbaja_id"])
            if resolucion:            
                logging.info("Creación de la extension de baja")
                expediente = resolucion["resolucion_expediente"] if resolucion else None
                resol = resolucion["resolucion_numero"] if resolucion else None      
                corresponde = resolucion["resolucion_corresponde"] if resolucion else None                         
                old_id = "extensionbaja_{}".format(e["extension_id"])
                desde = e["extension_fecha_baja"] if e["extension_fecha_baja"] else e["extension_fecha_hasta"]
                crear_designacion(session=session, desde=desde, hasta=None, old_id=old_id, historico=True, tipo=tipo_designacion[1], designacion_relacionada=ext.id, 
                        resolucion_id=e["extension_resolucionbaja_id"], observaciones="", categoria=categoria, expediente=expediente, resolucion=resol, corresponde=corresponde)
                ext.historico = True
        if e["extension_prorrogada_con"]:
            prorrogas_ext = obtener_prorrogas_de(d["extension_prorrogada_con"], cur)
            ext.historico = True
            for ep in prorrogas_ext:
                historico = ep["prorroga_prorrogada_con"] is None or ep["prorroga_resolucionbaja_id"] is not None
                old_id = "prorrogaextension_{}".format(ep["prorroga_id"])
                resolucion = obtener_resolucion(cur=cur, resolucion_id=ep["prorroga_resolucionbaja_id"])
                expediente = resolucion["resolucion_expediente"] if resolucion else None
                resol = resolucion["resolucion_numero"] if resolucion else None      
                corresponde = resolucion["resolucion_corresponde"] if resolucion else None                
                pro_ext = crear_designacion(session=session,desde=ep["prorroga_fecha_desde"], hasta=ep["prorroga_fecha_hasta"], old_id=old_id, historico=historico, tipo=tipo_designacion[4],
                                designacion_relacionada=ext.id, resolucion_id=ep["prorroga_resolucionalta_id"], observaciones="", expediente=expediente, resolucion=resol, corresponde=corresponde)            
                logging.info("Crear prorroga: {}".format(ep))                
                session.commit()
                
                # verifico si tiene una baja
                if ep["prorroga_resolucionbaja_id"]:
                    resolucion = obtener_resolucion(cur=cur, resolucion_id=ep["prorroga_resolucionbaja_id"])
                    if resolucion:                                
                        old_id = "extensionbaja_{}".format(p["prorroga_id"])
                        expediente = resolucion["resolucion_expediente"] if resolucion else None
                        resol = resolucion["resolucion_numero"] if resolucion else None      
                        corresponde = resolucion["resolucion_corresponde"] if resolucion else None                                                        
                        # si tiene baja creo la designacion baja y la relaciono con la prorroga
                        desde = ep["prorroga_fecha_baja"] if ep["prorroga_fecha_baja"] else ep["prorroga_fecha_hasta"]
                        categoria = None 
                        if ep["prorroga_tipobaja_id"]:
                            categoria = session.query(CategoriaDesignacion).filter(CategoriaDesignacion.old_id == str(p["prorroga_tipobaja_id"])).one_or_none()
                        crear_designacion(session=session, desde=desde, hasta=None, old_id=old_id, historico=False, tipo=tipo_designacion[4], designacion_relacionada=pro_ext.id,
                                resolucion_id=ep["prorroga_resolucionbaja_id"], observaciones="", categoria=categoria, expediente=expediente, resolucion=resol, corresponde=corresponde)            
    session.commit()


def importar_categorias(cur, s):
    logging.info("Importando categorias")
    cur.execute("SELECT tipobajadesig_id, tipobajadesig_nombre FROM tipo_baja")
    for c in cur:
        categoria = session.query(CategoriaDesignacion).filter(CategoriaDesignacion.old_id == str(c["tipobajadesig_id"])).one_or_none()
        if categoria is None:            
            categoria = CategoriaDesignacion()
            categoria.id = str(uuid.uuid4())
            categoria.old_id = str(c["tipobajadesig_id"])
            categoria.nombre = "Baja por {}".format(c["tipobajadesig_nombre"])
            session.add(categoria)
            logging.info(categoria.__dict__)
    session.commit()

if __name__ == '__main__':
    conn = psycopg2.connect("host='{}' user='{}' password='{}' dbname={}".format(
        os.environ['OLD_SILEG_DB_HOST'],
        os.environ['OLD_SILEG_DB_USER'],
        os.environ['OLD_SILEG_DB_PASSWORD'],
        os.environ['OLD_SILEG_DB_NAME']
    ))
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        with obtener_session() as session:
            importar_categorias(cur, session)
            
            cur.execute(""" SELECT * 
            FROM designacion_docente where desig_id =  179
            """)
            for d in cur:
                importar_designacion(d, cur, session)

    finally:
        cur.close()
        conn.close()        

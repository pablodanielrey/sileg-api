import psycopg2
from psycopg2.extras import DictCursor
import os
import uuid
import datetime
from sileg.model.entities import Designacion, CategoriaDesignacion, Lugar
import logging
logging.getLogger().setLevel(logging.DEBUG)
from sileg.model import obtener_session

tipo_designacion = ['original', 'baja', 'prorroga', 'extension', 'prorroga de extension']

def crear_designacion(session=None,desde=None, hasta=None, old_id=None, historico=False, tipo=tipo_designacion[0], 
                    designacion_relacionada=None, resolucion_id=None, observaciones='', categoria=None):
    d = session.query(Designacion).filter(Designacion.old_id == old_id).one_or_none()
    if d is None:
        d = Designacion()        
        d.old_id = old_id
        
    d.desde = desde
    d.hasta = hasta
    d.historico = historico
    d.tipo = tipo
    d.designacion_id = designacion_relacionada
    d.categorias = [categoria] if categoria else []
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

def importar_designacion(d, cur, session):
    logging.info("Importando designacion: {}".format(d))
    id = d["desig_id"]
    old_id = "desig_{}".format(id)
    desig = crear_designacion(session=session, desde=d["desig_fecha_desde"], hasta=d["desig_fecha_hasta"], old_id=old_id, historico=False, tipo=tipo_designacion[0], 
                            designacion_relacionada=None, resolucion_id=d["desig_resolucionalta_id"], observaciones=d["desig_observaciones"])

    logging.info("Desginacion creada: {}".format(desig.__dict__))    
    session.commit()
    if d["desig_resolucionbaja_id"]:
        logging.info("Crear baja: {}".format(d))
        old_id = "baja_{}".format(id)
        desde = d["desig_fecha_baja"] if d["desig_fecha_baja"] else d["desig_fecha_hasta"]
        categoria = None 
        if d["desig_tipobaja_id"]:
            categoria = session.query(CategoriaDesignacion).filter(CategoriaDesignacion.old_id == str(d["desig_tipobaja_id"])).one_or_none()
        crear_designacion(session=session, desde=desde, hasta=None, old_id=old_id, historico=True, tipo=tipo_designacion[1], designacion_relacionada=desig.id, 
                         resolucion_id=d["desig_resolucionbaja_id"], observaciones=d["desig_observaciones"], categoria=categoria)
        desig.historico = True

    prorrogas = []
    if d["desig_prorrogada_con"]:
        prorrogas = obtener_prorrogas_de(d["desig_prorrogada_con"], cur)
        for p in prorrogas:
            historico = p["prorroga_prorrogada_con"] is None or p["prorroga_resolucionbaja_id"] is not None
            old_id = "prorroga_{}".format(p["prorroga_id"])
            pro_desig = crear_designacion(session=session,desde=p["prorroga_fecha_desde"], hasta=p["prorroga_fecha_hasta"], old_id=old_id, historico=historico, tipo=tipo_designacion[2],
                              designacion_relacionada=desig.id, resolucion_id=d["desig_resolucionalta_id"], observaciones=d["desig_observaciones"])            
            logging.info("Crear prorroga: {}".format(p))
            session.commit()
            # verifico si tiene una baja
            if p["prorroga_resolucionbaja_id"]:
                old_id = "baja_{}".format(p["prorroga_id"])
                # si tiene baja creo la designacion baja y la relaciono con la prorroga
                desde = p["prorroga_fecha_baja"] if p["prorroga_fecha_baja"] else p["prorroga_fecha_hasta"]
                categoria = None 
                if p["prorroga_tipobaja_id"]:
                    categoria = session.query(CategoriaDesignacion).filter(CategoriaDesignacion.old_id == str(p["prorroga_tipobaja_id"])).one_or_none()
                crear_designacion(session=session, desde=desde, hasta=None, old_id=old_id, historico=False, tipo=tipo_designacion[1],
                         designacion_relacionada=desig.id, resolucion_id=d["desig_resolucionbaja_id"], observaciones=d["desig_observaciones"], categoria=categoria)
    session.commit()        

    extensiones = obtener_extensiones(id, cur)
    for e in extensiones:
        if e["extension_prorrogada_con"]:
            prorrogas_ext = obtener_prorrogas_de(d["extension_prorrogada_con"], cur)
            logging.info("Creo extension: {}".format(e))
            for ep in prorrogas_ext:
                logging.info("Creo extension prorroga {}".format(ep))


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
            FROM designacion_docente where desig_id =  108
            """)
            for d in cur:
                importar_designacion(d, cur, session)

    finally:
        cur.close()
        conn.close()        

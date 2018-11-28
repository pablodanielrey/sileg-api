
import psycopg2
from psycopg2.extras import DictCursor
import logging
logging.getLogger().setLevel(logging.DEBUG)

from sqlalchemy import or_
from sileg.model import obtener_session
from sileg.model.entities import Lugar, Facultad, LugarDictado, Departamento, Instituto, Oficina
import os
import uuid

def crear_lugares(s, padre_id, lugares):
    for l in lugares:
        c = s.query(Lugar).filter(Lugar.id == l['lugar'].id).one_or_none()
        if c:
            c.nombre = l['lugar'].nombre
        else:
            s.add(l['lugar'])

def importar_centros_regionales(s, cur, padre):
    sql = "select dpto_id, dpto_nombre from departamento where dpto_nombre like 'C. %'"    
    cur.execute(sql)
    for r in cur:
        old_id = 'dpto{}'.format(r["dpto_id"])
        logging.info("Centro id:{} nombre:{}".format(old_id, r["dpto_nombre"]))
        c = s.query(Lugar).filter(Lugar.old_id == old_id).one_or_none()
        if not c:
            logging.info("Creando centro regional: {}".format(r["dpto_nombre"]))            
            c = LugarDictado(nombre=r["dpto_nombre"])
            c.id = str(uuid.uuid4())
            c.padre_id = padre.id
            c.old_id = old_id
            s.add(c)

def importar_departamentos(s, cur, padre):
    sql = "select dpto_id, dpto_nombre from departamento where dpto_nombre like 'Departamento %'"    
    cur.execute(sql)
    for r in cur:
        old_id = 'dpto{}'.format(r["dpto_id"])
        logging.info("Departamento id:{} nombre:{}".format(old_id, r["dpto_nombre"]))
        c = s.query(Lugar).filter(Lugar.old_id == old_id).one_or_none()
        if not c:
            logging.info("Creando departamento: {}".format(r["dpto_nombre"]))            
            c = Departamento(nombre=r["dpto_nombre"])
            c.id = str(uuid.uuid4())
            c.padre_id = padre.id
            c.old_id = old_id
            s.add(c)    

def importar_institutos(s, cur, padre):
    sql = "select dpto_id, dpto_nombre from departamento where dpto_nombre like 'Instituto %'"    
    cur.execute(sql)
    for r in cur:
        old_id = 'dpto{}'.format(r["dpto_id"])
        logging.info("Instituto id:{} nombre:{}".format(old_id, r["dpto_nombre"]))
        c = s.query(Lugar).filter(Lugar.old_id == old_id).one_or_none()
        if not c:
            logging.info("Creando instituto: {}".format(r["dpto_nombre"]))
            c = Instituto(nombre=r["dpto_nombre"])
            c.id = str(uuid.uuid4())
            c.padre_id = padre.id
            c.old_id = old_id
            s.add(c)           

def importar_lugares(s, cur, raiz):
    sql = "select lugdetrab_id as id, lugdetrab_nombre as nombre, dpto_id from lugar_de_trabajo l left outer join departamento d on (l.lugdetrab_dpto_id = dpto_id)"
    cur.execute(sql)
    for r in cur:
        old_id = 'lugar{}'.format(r["id"])
        logging.info("Lugar id:{} nombre:{}".format(old_id, r["nombre"]))
        c = s.query(Lugar).filter(Lugar.old_id == old_id).one_or_none()
        if not c:
            padre = None            
            if r["dpto_id"] is not None:
                padre_id = 'dpto{}'.format(r["dpto_id"])
                padre = s.query(Lugar).filter(Lugar.old_id == padre_id).one_or_none()

            c = Oficina(r["nombre"])
            c.id = str(uuid.uuid4())
            c.padre_id = padre.id if padre else raiz.id
            c.old_id = old_id
            logging.info("Oficina a crear: {}".format(c.__dict__))
            s.add(c)

def importar_materias(s, cur, raiz):
    pass

if __name__ == '__main__':

    """ creo los lugares """

    raiz = {
        'lugar': Facultad(id='786fbe25-18f5-4aee-8a6a-050c39bf2406', nombre='SILEG'),
        'hijos': []
    }
         

    pid = None
    with obtener_session() as s:
        crear_lugares(s, pid, [raiz])
        if len(raiz['hijos']) > 0:
            pid = raiz['lugar'].id
            crear_lugares(s, pid, raiz['hijos'])        
        s.commit()

        conn = psycopg2.connect("host='{}' user='{}' password='{}' dbname={}".format(
            os.environ['OLD_SILEG_DB_HOST'],
            os.environ['OLD_SILEG_DB_USER'],
            os.environ['OLD_SILEG_DB_PASSWORD'],
            os.environ['OLD_SILEG_DB_NAME']
        ))
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:              
            logging.info("Importar centros regionales")  
            importar_centros_regionales(s, cur, raiz['lugar'])
            s.commit()
            logging.info("Importar centros departamentos")  
            importar_departamentos(s, cur, raiz['lugar'])
            s.commit()
            logging.info("Importar centros institutos")  
            importar_institutos(s, cur, raiz['lugar'])
            s.commit()
            logging.info("Importar lugares de trabajo")
            importar_lugares(s,cur, raiz['lugar'])  
            s.commit()
            importar_materias(s,cur, raiz['lugar'])
        finally:
            cur.close()
            conn.close()        
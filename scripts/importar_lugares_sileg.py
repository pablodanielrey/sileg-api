
import psycopg2
from psycopg2.extras import DictCursor
import logging
logging.getLogger().setLevel(logging.DEBUG)

from sqlalchemy import or_, and_
from sqlalchemy import func

from sileg.model import obtener_session
from sileg.model.entities import Lugar, Facultad, LugarDictado, Departamento, Instituto, Oficina, Materia, Catedra, Categoria
import os
import uuid

categoria_centro_id = '2d4fa072-740a-421d-a63e-1059717a6d8d'
categoria_dpto_id = 'f948ac90-82c1-42ea-a34a-018c17eb36d7'
categoria_inst_id = '582a7772-6f92-4bda-8896-917b405384a0'
categoria_lugares_id = '2b3fab6f-5545-453a-b672-4539d6850bab'

def crear_lugares(s, padre_id, lugares):
    for l in lugares:
        c = s.query(Lugar).filter(Lugar.id == l['lugar'].id).one_or_none()
        if c:
            c.nombre = l['lugar'].nombre
        else:
            s.add(l['lugar'])

def importar_centros_regionales(s, cur, padre):    
    sql = "select dpto_id, dpto_nombre from departamento where lower(dpto_nombre) like 'c. %' or lower(dpto_nombre) like 'c.u.%'"    
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
        else:
            c.padre_id = padre.id
            c.old_id = old_id            

def importar_departamentos(s, cur, padre):
    sql = "select dpto_id, dpto_nombre from departamento where dpto_nombre like 'Departamento %'"    
    cur.execute(sql)
    for r in cur:
        old_id = 'dpto{}'.format(r["dpto_id"])
        logging.info("Departamento id:{} nombre:{}".format(old_id, r["dpto_nombre"]))
        d = s.query(Lugar).filter(Lugar.old_id == old_id).one_or_none()
        if not d:
            logging.info("Creando departamento: {}".format(r["dpto_nombre"]))            
            d = Departamento(nombre=r["dpto_nombre"])
            d.id = str(uuid.uuid4())
            d.padre_id = padre.id
            d.old_id = old_id
            s.add(d)   
        else:
            d.padre_id = padre.id
            d.old_id = old_id             

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
        else:
            c.padre_id = padre.id
            c.old_id = old_id            

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
        else:
            padre = None            
            if r["dpto_id"] is not None:
                padre_id = 'dpto{}'.format(r["dpto_id"])
                padre = s.query(Lugar).filter(Lugar.old_id == padre_id).one_or_none()

            c.padre_id = padre.id if padre else raiz.id
            c.old_id = old_id            

def importar_materias(s, cur):
    sql = "select materia_id as id, materia_nombre as nombre from materia"
    cur.execute(sql)
    for r in cur:
        id = str(r["id"])
        mat = s.query(Materia).filter(or_(func.lower(Materia.nombre) == r['nombre'].lower() , Materia.old_id == id)).one_or_none()
        if mat:
            logging.info("Actualizar materia {}".format(r["nombre"]))
            mat.nombre = r["nombre"]
            mat.old_id = id
        else:
            logging.info("Crear materia {}".format(r["nombre"]))
            mat = Materia()
            mat.nombre = r["nombre"]
            mat.old_id = id
            s.add(mat)                        

def importar_catedras(s, cur, raiz):
    sql = """select catxmat_id as id, materia_dpto_id as dpto_id, materia_nombre, materia_id, c.catedra_nombre as catedra \
            from catedras_x_materia cm \
            inner join materia m on (m.materia_id = cm.catxmat_materia_id) \
            inner join catedra c on (c.catedra_id = cm.catxmat_catedra_id)
    """
    cur.execute(sql)
    for r in cur:  

        materia = s.query(Materia).filter(Materia.old_id == str(r['materia_id'])).one_or_none()
        if materia is None:
            logging.info("No existe la materia {}".format(r["materia_nombre"]))
            continue
        
        dpto_old_id = 'dpto{}'.format(r["dpto_id"])
        padre = s.query(Lugar).filter(Lugar.old_id == dpto_old_id).one_or_none()
        padre_id = padre.id if padre else raiz.id

        old_id = str(r["id"])
        nombre = "{} {}".format(r["materia_nombre"], r["catedra"])

        l = s.query(Catedra).filter(or_(and_(func.lower(Catedra.nombre) == r['catedra'].lower(),Catedra.materia_id == materia.id),Catedra.old_id == old_id)).one_or_none()

        if l:
            l.old_id = old_id
            l.nombre = nombre
            l.padre_id = padre_id
            l.materia_id = materia.id
            logging.info("Catedra actualizada: {}".format(l.__dict__))
        else:
            l = Catedra(nombre=nombre, materia_id=materia.id, padre_id=padre_id)
            l.old_id = old_id
            s.add(l)
            logging.info("Catedra creada: {}".format(l.__dict__))        

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
            padre_centro = s.query(Lugar).filter(Lugar.id == categoria_centro_id).one_or_none()
            if padre_centro is None:
                padre_centro = Categoria(id=categoria_centro_id, nombre="Centros Regionales")
                padre_centro.padre_id = raiz['lugar'].id
                s.add(padre_centro)
                s.commit()
            importar_centros_regionales(s, cur, padre_centro)
            s.commit()

            logging.info("Importar departamentos")  
            padre_dptos = s.query(Lugar).filter(Lugar.id == categoria_dpto_id).one_or_none()
            if padre_dptos is None:
                padre_dptos = Categoria(id=categoria_dpto_id, nombre="Departamentos")
                padre_dptos.padre_id = raiz['lugar'].id
                s.add(padre_dptos)
                s.commit()            
            importar_departamentos(s, cur, padre_dptos)
            s.commit()

            logging.info("Importar institutos")  
            padre_inst = s.query(Lugar).filter(Lugar.id == categoria_inst_id).one_or_none()
            if padre_inst is None:
                padre_inst = Categoria(id=categoria_inst_id, nombre="Institutos")
                padre_inst.padre_id = raiz['lugar'].id
                s.add(padre_inst)
                s.commit()               
            importar_institutos(s, cur, padre_inst)
            s.commit()
            
            logging.info("Importar lugares de trabajo")
            padre_lugares = s.query(Lugar).filter(Lugar.id == categoria_lugares_id).one_or_none()
            if padre_lugares is None:
                padre_lugares = Categoria(id=categoria_lugares_id, nombre="Lugares")
                padre_lugares.padre_id = raiz['lugar'].id
                s.add(padre_lugares)
                s.commit()                           
            importar_lugares(s,cur, padre_lugares)  
            s.commit()

            logging.info("Importar materias")
            importar_materias(s,cur)
            s.commit()
            logging.info("Importar catedras")
            importar_catedras(s,cur, raiz['lugar'])
            s.commit()
        finally:
            cur.close()
            conn.close()        





"""
Estas son las materias que quedaron sin old_id


sileg=# select * from materia where old_id is null order by nombre;
                  id                  |           creado           | actualizado |                                         nombre                                         | old_id 
--------------------------------------+----------------------------+-------------+----------------------------------------------------------------------------------------+--------
 165bbf19-b978-4ab7-90bd-d6c23e4ff109 | 2017-07-19 12:17:40.779934 |             | administración i (introducción a la administración y al estudio de las organizaciones) | 
 476c4b2b-f1a7-49f8-ae7c-762d188321a4 | 2017-07-19 12:17:41.346569 |             | administración i (introducción a la economía y al estructura económica argentina       | 
 af01103c-a044-4782-bdb9-adb740bd68f3 | 2017-07-19 12:17:30.205851 |             | contabilidad sup.i                                                                     | 
 d543f683-0881-47a7-abde-83a73e684ecc | 2017-07-19 12:17:48.122235 |             | contabilidad vi (costos para la gestión)                                               | 
 c96dd42f-9007-4cc3-b059-5490dad69a6d | 2017-07-19 12:17:49.063458 |             | contabilidad v (sistemas de información)                                               | 
 c6476ef2-3978-4096-93e7-8e5d992e8ed5 | 2017-07-19 12:15:44.813965 |             | matemática i(análisis)                                                                 | 
 2f1248c8-4b55-4280-99c0-d7a2a486df56 | 2017-07-19 12:17:25.364086 |             | matemática i(análisis matemático)                                                      | 
 39120b86-4390-482a-84aa-19b728b4cb53 | 2017-07-19 12:17:25.721907 |             | matemática ii(algebra)                                                                 | 
 ed8850f0-63c9-4f9a-b41b-618156b152df | 2017-07-19 12:15:58.398029 |             | seminario depto economia                                                               | 

"""

import sys
import logging
logging.getLogger().setLevel(logging.INFO)
import os
import psycopg2
import psycopg2.extras
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sileg.model.entities import Cargo, Catedra, Categoria, Departamento, Designacion, LugarDictado, Materia, Usuario, Secretaria, Instituto, Maestria, Prosecretaria, Escuela, Lugar, Direccion, Centro


engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
    os.environ['SILEG_DB_USER'],
    os.environ['SILEG_DB_PASSWORD'],
    os.environ['SILEG_DB_HOST'],
    os.environ['SILEG_DB_NAME']
), echo=False)

Session = sessionmaker(bind=engine)
session = Session();








def designacionesDocentes():
    """ conexion con la base antigua del sileg para obtener las designaciones docentes """
    host = os.environ['SILEG_VIEJO_DB_HOST']
    dbname = os.environ['SILEG_VIEJO_DB_NAME']
    user = os.environ['SILEG_VIEJO_DB_USER']
    password = os.environ['SILEG_VIEJO_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT desig_id AS id_designacion, desig_observaciones AS observaciones, desig_fecha_desde AS fecha_desde, desig_fecha_hasta AS fecha_hasta, desig_fecha_baja AS fecha_baja,
                resolucion_alta.resolucion_numero AS resolucion,  resolucion_alta.resolucion_expediente AS expediente,
                desig_ord_fdesde AS fecha_desde_ordenanza, desig_ord_fhasta AS fecha_hasta_ordenanza,
                resolucion_ordenanza.resolucion_numero AS resolucion_ordenanza, resolucion_ordenanza.resolucion_expediente AS expediente_ordenanza, 
                resolucion_baja.resolucion_numero AS resolucion_baja, resolucion_baja.resolucion_expediente AS expediente_baja,
                tipo_baja.tipobajadesig_nombre AS baja,
                tipocargo_nombre AS cargo, tipo_dedicacion.tipodedicacion_nombre AS dedicacion, tipocaracter_nombre AS caracter,
                tipo_caracter_extraordinario.tipoextraord_nombre AS caracter_extraordinario,
                pers_nombres AS nombres, pers_apellidos AS apellidos, pers_nrodoc AS numero_documento,
                materia.materia_nombre AS materia, catedra.catedra_nombre AS catedra, departamento.dpto_nombre AS departamento

                FROM designacion_docente
                INNER JOIN tipo_cargo ON (designacion_docente.desig_tipocargo_id = tipo_cargo.tipocargo_id)
                INNER JOIN tipo_dedicacion ON (designacion_docente.desig_tipodedicacion_id = tipo_dedicacion.tipodedicacion_id)
                INNER JOIN tipo_caracter ON (designacion_docente.desig_tipocaracter_id = tipo_caracter.tipocaracter_id)
                INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
                INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
                INNER JOIN catedras_x_materia ON (designacion_docente.desig_catxmat_id = catedras_x_materia.catxmat_id)
                INNER JOIN materia ON (catedras_x_materia.catxmat_materia_id = materia.materia_id)
                INNER JOIN catedra ON (catedras_x_materia.catxmat_catedra_id = catedra.catedra_id)
                INNER JOIN departamento ON (materia.materia_dpto_id = departamento.dpto_id)
               
                LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = desig_resolucionalta_id)
                LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = desig_resolucionbaja_id)
                LEFT JOIN resolucion AS resolucion_ordenanza ON (resolucion_ordenanza.resolucion_id = desig_resolucionord_id)
                LEFT JOIN tipo_caracter_extraordinario ON (designacion_docente.desig_tipodedicacion_id = tipo_caracter_extraordinario.tipoextraord_id)
                LEFT JOIN tipo_baja AS tipo_baja ON (designacion_docente.desig_tipobaja_id = tipo_baja.tipobajadesig_id)
            ''');

            return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()
        
        
        
        



def designacionesLugares():
    """ conexion con la base antigua del sileg para obtener las designaciones a un lugar de trabajo """
    host = os.environ['SILEG_VIEJO_DB_HOST']
    dbname = os.environ['SILEG_VIEJO_DB_NAME']
    user = os.environ['SILEG_VIEJO_DB_USER']
    password = os.environ['SILEG_VIEJO_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT desig_id AS id_designacion, desig_observaciones AS observaciones, desig_fecha_desde AS fecha_desde, desig_fecha_hasta AS fecha_hasta, desig_fecha_baja AS fecha_baja,
                resolucion_alta.resolucion_numero AS resolucion,  resolucion_alta.resolucion_expediente AS expediente,
                desig_ord_fdesde AS fecha_desde_ordenanza, desig_ord_fhasta AS fecha_hasta_ordenanza,
                resolucion_ordenanza.resolucion_numero AS resolucion_ordenanza, resolucion_ordenanza.resolucion_expediente AS resolucion_expediente, 
                resolucion_baja.resolucion_numero AS resolucion_baja, resolucion_baja.resolucion_expediente AS expediente_baja,
                tipo_baja.tipobajadesig_nombre AS baja,
                tipocargo_nombre AS cargo, tipo_dedicacion.tipodedicacion_nombre AS dedicacion, tipocaracter_nombre AS caracter,
                tipo_caracter_extraordinario.tipoextraord_nombre AS caracter_extraordinario,
                pers_nombres AS nombres, pers_apellidos AS apellidos, pers_nrodoc AS numero_documento,
                lugdetrab_nombre AS lugar, area_nombre AS area, funcion_nombre AS funcion
                
                FROM designacion_docente
                INNER JOIN tipo_cargo ON (desig_tipocargo_id = tipocargo_id)
                INNER JOIN tipo_dedicacion ON (desig_tipodedicacion_id = tipodedicacion_id)
                INNER JOIN tipo_caracter ON (desig_tipocaracter_id = tipocaracter_id)
                INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
                INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
                INNER JOIN lugar_de_trabajo ON (designacion_docente.desig_lugdetrab_id = lugar_de_trabajo.lugdetrab_id)
                LEFT JOIN area ON (lugar_de_trabajo.lugdetrab_area_id = area.area_id)
                LEFT JOIN funcion ON (designacion_docente.desig_funcion_id = funcion.funcion_id)
                
                LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = desig_resolucionalta_id)
                LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = desig_resolucionbaja_id)
                LEFT JOIN resolucion AS resolucion_ordenanza ON (resolucion_ordenanza.resolucion_id = desig_resolucionord_id)
                LEFT JOIN tipo_caracter_extraordinario ON (designacion_docente.desig_tipodedicacion_id = tipo_caracter_extraordinario.tipoextraord_id)
                LEFT JOIN tipo_baja ON (designacion_docente.desig_tipobaja_id = tipo_baja.tipobajadesig_id)
            ''');

            return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()
        
        
        
        
        
        


def extensionesDocentesDeDesignacionesDocentes():
    """ conexion con la base antigua del sileg para obtener las designaciones docentes """
    host = os.environ['SILEG_VIEJO_DB_HOST']
    dbname = os.environ['SILEG_VIEJO_DB_NAME']
    user = os.environ['SILEG_VIEJO_DB_USER']
    password = os.environ['SILEG_VIEJO_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT desig_id AS id_designacion,
                extension_id AS id_extension,
                extension.extension_fecha_desde AS fecha_desde, extension.extension_fecha_hasta AS fecha_hasta, extension.extension_fecha_baja AS fecha_baja,
                eresolucion_alta.resolucion_numero AS resolucion, eresolucion_alta.resolucion_expediente AS expediente,
                eresolucion_baja.resolucion_numero AS resolucion_baja, eresolucion_baja.resolucion_expediente AS expediente_baja,
                emateria.materia_nombre AS materia, ecatedra.catedra_nombre AS catedra, edepartamento.dpto_nombre AS departamento,
                etipo_dedicacion.tipodedicacion_nombre AS dedicacion, 
                etipo_baja.tipobajadesig_nombre AS baja,
                extension.extension_comision AS observaciones

                FROM designacion_docente
                INNER JOIN tipo_cargo ON (designacion_docente.desig_tipocargo_id = tipo_cargo.tipocargo_id)
                INNER JOIN tipo_dedicacion ON (designacion_docente.desig_tipodedicacion_id = tipo_dedicacion.tipodedicacion_id)
                INNER JOIN tipo_caracter ON (designacion_docente.desig_tipocaracter_id = tipo_caracter.tipocaracter_id)
                INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
                INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
                INNER JOIN catedras_x_materia ON (designacion_docente.desig_catxmat_id = catedras_x_materia.catxmat_id)
                INNER JOIN materia ON (catedras_x_materia.catxmat_materia_id = materia.materia_id)
                INNER JOIN catedra ON (catedras_x_materia.catxmat_catedra_id = catedra.catedra_id)
                INNER JOIN departamento ON (materia.materia_dpto_id = departamento.dpto_id)

                INNER JOIN extension ON (extension.extension_designacion_id = designacion_docente.desig_id)
                INNER JOIN catedras_x_materia AS ecatedras_x_materia ON (extension.extension_catxmat_id = ecatedras_x_materia.catxmat_id)
                INNER JOIN materia AS emateria ON (ecatedras_x_materia.catxmat_materia_id = emateria.materia_id)
                INNER JOIN catedra AS ecatedra ON (ecatedras_x_materia.catxmat_catedra_id = ecatedra.catedra_id)
                INNER JOIN departamento AS edepartamento ON (emateria.materia_dpto_id = edepartamento.dpto_id)
                INNER JOIN tipo_dedicacion AS etipo_dedicacion ON (extension.extension_nuevadedicacion_id = etipo_dedicacion.tipodedicacion_id)
                
                LEFT JOIN resolucion AS eresolucion_alta ON (eresolucion_alta.resolucion_id = extension_resolucionalta_id)
                LEFT JOIN resolucion AS eresolucion_baja ON (eresolucion_baja.resolucion_id = extension_resolucionbaja_id)
                LEFT JOIN tipo_baja AS etipo_baja ON (extension.extension_tipobaja_id = etipo_baja.tipobajadesig_id);
            ''');

            return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()





def extensionesDocentesDeDesignacionesLugares():
    """ conexion con la base antigua del sileg para obtener las designaciones docentes """
    host = os.environ['SILEG_VIEJO_DB_HOST']
    dbname = os.environ['SILEG_VIEJO_DB_NAME']
    user = os.environ['SILEG_VIEJO_DB_USER']
    password = os.environ['SILEG_VIEJO_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT desig_id AS id_designacion,
	              extension_id AS id_extension,
                extension.extension_fecha_desde AS fecha_desde, extension.extension_fecha_hasta AS fecha_hasta, extension.extension_fecha_baja AS fecha_baja,
                eresolucion_alta.resolucion_numero AS resolucion, eresolucion_alta.resolucion_expediente AS expediente,
                eresolucion_baja.resolucion_numero AS resolucion_baja, eresolucion_baja.resolucion_expediente AS expediente_baja,
                emateria.materia_nombre AS materia, ecatedra.catedra_nombre AS catedra, edepartamento.dpto_nombre AS departamento,
                etipo_dedicacion.tipodedicacion_nombre AS dedicacion, 
                etipo_baja.tipobajadesig_nombre AS baja,
                extension.extension_comision AS observaciones
                
                FROM designacion_docente
                INNER JOIN tipo_cargo ON (desig_tipocargo_id = tipocargo_id)
                INNER JOIN tipo_dedicacion ON (desig_tipodedicacion_id = tipodedicacion_id)
                INNER JOIN tipo_caracter ON (desig_tipocaracter_id = tipocaracter_id)
                INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
                INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
                INNER JOIN lugar_de_trabajo ON (designacion_docente.desig_lugdetrab_id = lugar_de_trabajo.lugdetrab_id)
                
		            INNER JOIN extension ON (extension.extension_designacion_id = designacion_docente.desig_id)
                INNER JOIN catedras_x_materia AS ecatedras_x_materia ON (extension.extension_catxmat_id = ecatedras_x_materia.catxmat_id)
                INNER JOIN materia AS emateria ON (ecatedras_x_materia.catxmat_materia_id = emateria.materia_id)
                INNER JOIN catedra AS ecatedra ON (ecatedras_x_materia.catxmat_catedra_id = ecatedra.catedra_id)
                INNER JOIN departamento AS edepartamento ON (emateria.materia_dpto_id = edepartamento.dpto_id)
                INNER JOIN tipo_dedicacion AS etipo_dedicacion ON (extension.extension_nuevadedicacion_id = etipo_dedicacion.tipodedicacion_id)
                
                LEFT JOIN resolucion AS eresolucion_alta ON (eresolucion_alta.resolucion_id = extension_resolucionalta_id)
                LEFT JOIN resolucion AS eresolucion_baja ON (eresolucion_baja.resolucion_id = extension_resolucionbaja_id)
                LEFT JOIN tipo_baja AS etipo_baja ON (extension.extension_tipobaja_id = etipo_baja.tipobajadesig_id);
            ''');

            return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()






def extensionesLugaresDeDesignacionesDocentes():
    """ conexion con la base antigua del sileg para obtener las designaciones docentes """
    host = os.environ['SILEG_VIEJO_DB_HOST']
    dbname = os.environ['SILEG_VIEJO_DB_NAME']
    user = os.environ['SILEG_VIEJO_DB_USER']
    password = os.environ['SILEG_VIEJO_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT desig_id AS id_designacion,
                extension_id AS id_extension,
                extension.extension_fecha_desde AS fecha_desde, extension.extension_fecha_hasta AS fecha_hasta, extension.extension_fecha_baja AS fecha_baja,
                eresolucion_alta.resolucion_numero AS resolucion, eresolucion_alta.resolucion_expediente AS expediente,
                eresolucion_baja.resolucion_numero AS resolucion_baja, eresolucion_baja.resolucion_expediente AS expediente_baja,
                elugar_de_trabajo.lugdetrab_nombre AS lugar, earea.area_nombre AS area, efuncion.funcion_nombre AS funcion,
                etipo_dedicacion.tipodedicacion_nombre AS dedicacion, 
                etipo_baja.tipobajadesig_nombre AS baja,
                extension.extension_comision AS observaciones          
                
                FROM designacion_docente
                INNER JOIN tipo_cargo ON (designacion_docente.desig_tipocargo_id = tipo_cargo.tipocargo_id)
                INNER JOIN tipo_dedicacion ON (designacion_docente.desig_tipodedicacion_id = tipo_dedicacion.tipodedicacion_id)
                INNER JOIN tipo_caracter ON (designacion_docente.desig_tipocaracter_id = tipo_caracter.tipocaracter_id)
                INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
                INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
                INNER JOIN catedras_x_materia ON (designacion_docente.desig_catxmat_id = catedras_x_materia.catxmat_id)
                INNER JOIN materia ON (catedras_x_materia.catxmat_materia_id = materia.materia_id)
                INNER JOIN catedra ON (catedras_x_materia.catxmat_catedra_id = catedra.catedra_id)
                INNER JOIN departamento ON (materia.materia_dpto_id = departamento.dpto_id)
                
		            INNER JOIN extension ON (extension.extension_designacion_id = designacion_docente.desig_id)
                INNER JOIN lugar_de_trabajo AS elugar_de_trabajo ON (extension.extension_lugdetrab_id = elugar_de_trabajo.lugdetrab_id)
                LEFT JOIN area AS earea ON (elugar_de_trabajo.lugdetrab_area_id = earea.area_id)
                LEFT JOIN funcion AS efuncion ON (extension.extension_funcion_id = efuncion.funcion_id)
                INNER JOIN tipo_dedicacion AS etipo_dedicacion ON (extension.extension_nuevadedicacion_id = etipo_dedicacion.tipodedicacion_id)
                
                LEFT JOIN resolucion AS eresolucion_alta ON (eresolucion_alta.resolucion_id = extension_resolucionalta_id)
                LEFT JOIN resolucion AS eresolucion_baja ON (eresolucion_baja.resolucion_id = extension_resolucionbaja_id)
                LEFT JOIN tipo_baja AS etipo_baja ON (extension.extension_tipobaja_id = etipo_baja.tipobajadesig_id);
            ''');

            return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()
        
        



def extensionesLugaresDeDesignacionesLugares():
    """ conexion con la base antigua del sileg para obtener las designaciones """
    host = os.environ['SILEG_VIEJO_DB_HOST']
    dbname = os.environ['SILEG_VIEJO_DB_NAME']
    user = os.environ['SILEG_VIEJO_DB_USER']
    password = os.environ['SILEG_VIEJO_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT desig_id AS id_designacion,
                extension_id AS id_extension,
                extension.extension_fecha_desde AS fecha_desde, extension.extension_fecha_hasta AS fecha_hasta, extension.extension_fecha_baja AS fecha_baja,
                eresolucion_alta.resolucion_numero AS resolucion, eresolucion_alta.resolucion_expediente AS expediente,
                eresolucion_baja.resolucion_numero AS resolucion_baja, eresolucion_baja.resolucion_expediente AS expediente_baja,
                elugar_de_trabajo.lugdetrab_nombre AS lugar, earea.area_nombre AS area, efuncion.funcion_nombre AS funcion,
                etipo_dedicacion.tipodedicacion_nombre AS dedicacion, 
                etipo_baja.tipobajadesig_nombre AS baja,
                extension.extension_comision AS observaciones                                                             
                
                FROM designacion_docente
                INNER JOIN tipo_cargo ON (desig_tipocargo_id = tipocargo_id)
                INNER JOIN tipo_dedicacion ON (desig_tipodedicacion_id = tipodedicacion_id)
                INNER JOIN tipo_caracter ON (desig_tipocaracter_id = tipocaracter_id)
                INNER JOIN empleado ON (designacion_docente.desig_empleado_id = empleado.empleado_id)
                INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
                INNER JOIN lugar_de_trabajo ON (designacion_docente.desig_lugdetrab_id = lugar_de_trabajo.lugdetrab_id)

		            INNER JOIN extension ON (extension.extension_designacion_id = designacion_docente.desig_id)
                INNER JOIN lugar_de_trabajo AS elugar_de_trabajo ON (extension.extension_lugdetrab_id = elugar_de_trabajo.lugdetrab_id)
                LEFT JOIN area AS earea ON (elugar_de_trabajo.lugdetrab_area_id = earea.area_id)
                LEFT JOIN funcion AS efuncion ON (extension.extension_funcion_id = efuncion.funcion_id)
                INNER JOIN tipo_dedicacion AS etipo_dedicacion ON (extension.extension_nuevadedicacion_id = etipo_dedicacion.tipodedicacion_id)
               
                LEFT JOIN resolucion AS eresolucion_alta ON (eresolucion_alta.resolucion_id = extension_resolucionalta_id)
                LEFT JOIN resolucion AS eresolucion_baja ON (eresolucion_baja.resolucion_id = extension_resolucionbaja_id)
                LEFT JOIN tipo_baja AS etipo_baja ON (extension.extension_tipobaja_id = etipo_baja.tipobajadesig_id);
            ''');

            return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()




def prorrogasIniciales(tipoDesignacion):
    """ tipoDesignacion = 'des' | 'ext' | 'pro' """
    host = os.environ['SILEG_VIEJO_DB_HOST']
    dbname = os.environ['SILEG_VIEJO_DB_NAME']
    user = os.environ['SILEG_VIEJO_DB_USER']
    password = os.environ['SILEG_VIEJO_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT 
                prorroga_id AS id_prorroga, 
                prorroga_fecha_obtencion AS observaciones,
                prorroga_fecha_desde AS fecha_desde,
                prorroga_fecha_hasta AS fecha_hasta,
                resolucion_alta.resolucion_numero AS resolucion,  resolucion_alta.resolucion_expediente AS expediente,
                resolucion_baja.resolucion_numero AS resolucion_baja, resolucion_baja.resolucion_expediente AS expediente_baja,
                prorroga_prorroga_de_id AS id_designacion,
                pers_nombres AS nombres, pers_apellidos AS apellidos, pers_nrodoc AS numero_documento
                FROM prorroga
                INNER JOIN empleado ON (prorroga.prorroga_idemp = empleado.empleado_id)  
                INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
                LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = prorroga_resolucionalta_id)
                LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = prorroga_resolucionbaja_id)
                AND prorroga_prorroga_de = %s;
            ''', (tipoDesignacion,));

            return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()
      
        
        



def prorrogasDeIds(ids):
    host = os.environ['SILEG_VIEJO_DB_HOST']
    dbname = os.environ['SILEG_VIEJO_DB_NAME']
    user = os.environ['SILEG_VIEJO_DB_USER']
    password = os.environ['SILEG_VIEJO_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT 
                prorroga_id AS id_prorroga, 
                prorroga_fecha_obtencion AS observaciones,
                prorroga_fecha_desde AS fecha_desde,
                prorroga_fecha_hasta AS fecha_hasta,
                resolucion_alta.resolucion_numero AS resolucion,  resolucion_alta.resolucion_expediente AS expediente,
                resolucion_baja.resolucion_numero AS resolucion_baja, resolucion_baja.resolucion_expediente AS expediente_baja,
                prorroga_prorroga_de_id AS id_designacion,
                pers_nombres AS nombres, pers_apellidos AS apellidos, pers_nrodoc AS numero_documento
                FROM prorroga
                INNER JOIN empleado ON (prorroga.prorroga_idemp = empleado.empleado_id)  
                INNER JOIN persona ON (empleado.empleado_pers_id = persona.pers_id)
                LEFT JOIN resolucion AS resolucion_alta ON (resolucion_alta.resolucion_id = prorroga_resolucionalta_id)
                LEFT JOIN resolucion AS resolucion_baja ON (resolucion_baja.resolucion_id = prorroga_resolucionbaja_id)
                AND prorroga_prorroga_de_id IN (%s);
            ''', (tuple(ids),));

            return cur.fetchall()
        finally:
          cur.close()

    finally:
        conn.close()
      





  






#consulta de todos los usuarios de profile.users, retorna un array de la forma users[dni] = id
def users():
    host = os.environ['SILEG_DB_HOST']
    dbname = os.environ['SILEG_DB_NAME']
    user = os.environ['SILEG_DB_USER']
    password = os.environ['SILEG_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''
                SELECT id, dni FROM profile.users
            ''');

            users = {}
            for u in cur:
                users[u["dni"]] = u["id"]

            return users
        finally:
          cur.close()
    finally:
        conn.close()


#consulta de todos los usuarios de profile.users, retorna un array de la forma users[dni] = id
def insertUsuario(dni, nombres, apellidos):
    host = os.environ['SILEG_DB_HOST']
    dbname = os.environ['SILEG_DB_NAME']
    user = os.environ['SILEG_DB_USER']
    password = os.environ['SILEG_DB_PASSWORD']
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            id = str(uuid.uuid4())

            cur.execute('''
                INSERT INTO profile.users (id, dni, name, lastname) VALUES (%s, %s, %s, %s)
            ''', (id, dni, nombres, apellidos))
            cur.commit()          
            return id
        finally:
          cur.close()
    finally:
        conn.close()
        
        
        


def setUsuario(datos, users):
    """
        SI NO EXISTE NO SE CREA DIRECTAMENTE EN LA BASE SIN USAR SQLALCHEMY
        
        carga el usuario dentro de las tablas internas del sistema chequeando con el sistema de perfiles de usuario principal.

        consulta para verificar:

         select u.dni, u.name, u.lastname, m.email
            from sileg.usuario s
            left join profile.users u on (s.id = u.id)
            left join profile.mails m on (u.id = m.user_id);
    """
    
    dni = str(datos['numero_documento'])
    if dni not in users:
        print('no existe el usuario dni ' + dni + ', se agregara directamente en profile.users\n')
        userId = insertUsuario(dni, datos['nombres'], datos['apellidos'])
        users[dni] =id
    else:
        userId = users[dni]

    usuario = session.query(Usuario).filter_by(id=userId).first()
    if not usuario:
        print('no existe el usuario en el sileg nuevo, se cargara: ' + userId + ' ' + dni + '\n')
        usuario = Usuario(id=userId)
        session.add(usuario)
        session.commit()  
    return usuario







def setLugarDocente(datos):
    """
    Define lugar a partir de las designaciones docentes
    """
    
    mat_ = datos["materia"].split("C.U.")
    dep = datos['departamento'].strip().lower()
    cat = datos['catedra'].strip().lower()

    
    
    mat = None
    lugDic = None
    if len(mat_) > 1:
        """
            la designación del sileg tiene en
                depto_nombre = centro regional  (se descarta porque el centro regional ---> lugar dictado = esa info sale del nombre materia)
                catedra_nombre --> Catedra
                materia_nombre --> Materia y lugarDictado
                Departamento no se puede obtener de ningun lado de la designacion. esa info no existe

                forma de verificar los datos en la base
                select m.id, m.nombre, l.id, l.nombre, ld.id, ld.nombre from sileg.catedra c left join sileg.lugar l on (l.id = c.id) left join sileg.materia m on (c.materia_id = m.id) left join sileg.lugar ld on (ld.padre_id = c.id);
        """

        mat = mat_[0].replace('-','').strip().lower()
        lugDic = mat_[1].strip().lower()

        #agregar materia
        materia = session.query(Materia).filter_by(nombre=mat).first()
        if not materia:
            print('no existe materia, se cargara: ' +  mat  + '\n')
            materia = Materia(nombre=mat)
            session.add(materia)
            session.commit()  
            
        #agregar catedra
        catedra = session.query(Catedra).filter_by(nombre=cat, materia_id=materia.id).first()
        if not catedra:
            print('no existe catedra, se cargara: ' +  cat  + '\n')
            catedra = Catedra(nombre=cat, materia_id=materia.id)
            session.add(catedra)
            session.commit()  
            
        lugarDictado = session.query(LugarDictado).filter_by(nombre=lugDic, padre_id=catedra.id).first()
        if not lugarDictado:
            print('no existe lugar dictado, se cargara: ' +  lugDic  + '\n')
            lugarDictado = LugarDictado(nombre=lugDic, padre_id=catedra.id)
            session.add(lugarDictado)
            session.commit()  
            
        return lugarDictado

    else:
        """
            la designación del sileg tiene en
                depto_nombre --> Departamento
                catedra_nombre --> Catedra
                materia_nombre --> Materia


                forma de verificar

                select ld.id, ld.nombre, m.id, m.nombre, c.id, l.nombre
                    from sileg.catedra c left join sileg.lugar l on (c.id = l.id)
                    left join sileg.materia m on (m.id = c.materia_id)
                    left join sileg.lugar ld on (ld.id = l.padre_id)

        """
        mat = mat_[0].strip().lower()

        #agregar departamento
        departamento = session.query(Departamento).filter_by(nombre=dep).first()
        if not departamento:
            print('no existe departamento, se cargara: ' +  dep  + '\n')
            departamento = Departamento(nombre=dep)
            session.add(departamento)
            session.commit()  
            
        #agregar materia
        materia = session.query(Materia).filter_by(nombre=mat).first()
        if not materia:
            print('no existe materia, se cargara: ' +  mat  + '\n')
            materia = Materia(nombre=mat)
            session.add(materia)
            session.commit()  
            
        #agregar catedra
        catedra = session.query(Catedra).filter_by(nombre=cat, materia_id=materia.id).first()
        if not catedra:
            print('no existe catedra, se cargara: ' +  cat  + '\n')
            catedra = Catedra(nombre=cat, materia_id=materia.id, padre_id=departamento.id)
            session.add(catedra)
            session.commit()  
            
        return catedra







def setLugarTrabajo(datos):
    """
    Define lugar a partir de las designaciones a lugar de trabajo
    """

    lug = datos["lugar"].strip().lower()
    area = datos['area'].strip().lower()
    #func = datos['funcion'].strip().lower()

    lugar = None

    if area == "secretaria" or area == "secretaría":
        if area not in lug:
            lug = "secretaría de " + lug
            
        lugar = session.query(Secretaria).filter_by(nombre=lug).first() 
        if not lugar:
            print('no existe secretaria, se cargara: ' +  lug  + '\n')
            lugar = Secretaria(nombre=lug)
            session.add(lugar)
            session.commit()                  

    elif area == "prosecretaria" or area == "prosecretaría":
        if area not in lug:
            lug = "prosecretaría de " + lug
            
        lugar = session.query(Prosecretaria).filter_by(nombre=lug).first() 
        if not lugar:
            print('no existe prosecretaria, se cargara: ' +  lug  + '\n')
            lugar = Prosecretaria(nombre=lug)
            session.add(lugar)
            session.commit()            
                
    elif area == "maestria" or area == "maestría":
        if area not in lug:
            lug = "maestría en " + lug
            
        lugar = session.query(Maestria).filter_by(nombre=lug).first() 
        if not lugar:
            print('no existe maestria, se cargara: ' +  lug  + '\n')
            lugar = Maestria(nombre=lug)
            session.add(lugar)
            session.commit()              
            
    elif area == "instituto":
        if area not in lug:
            lug = "instituto de " + lug
            
        lugar = session.query(Instituto).filter_by(nombre=lug).first() 
        if not lugar:
            print('no existe instituto, se cargara: ' +  lug  + '\n')
            lugar = Instituto(nombre=lug)
            session.add(lugar)
            session.commit()
                
    elif area == "escuela":
        if area not in lug:
            lug = "escuela de " + lug
            
        lugar = session.query(Escuela).filter_by(nombre=lug).first() 
        if not lugar:
            print('no existe escuela, se cargara: ' +  lug  + '\n')
            lugar = Escuela(nombre=lug)
            session.add(lugar)
            session.commit()
                
    elif area == "direccion" or area == "dirección":
        if area not in lug:
            lug = "dirección de " + lug
            
        lugar = session.query(Direccion).filter_by(nombre=lug).first() 
        if not lugar:
            print('no existe direccion, se cargara: ' +  lug  + '\n')       
            lugar = Direccion(nombre=lug)
            session.add(lugar)
            session.commit()
                
    elif area == "departamento":
        if area not in lug:
            lug = "departamento de " + lug
        
        lugar = session.query(Departamento).filter_by(nombre=lug).first() 
        if not lugar:
            print('no existe departamento, se cargara: ' +  lug  + '\n')
            lugar = Departamento(nombre=lug)
            session.add(lugar)
            session.commit()
            
    elif area == "centro":
        if "centro" not in lug:
            lug = "centro de " + lug
        
        lugar = session.query(Centro).filter_by(nombre=lug).first() 
        if not lugar:
            print('no existe centro, se cargara: ' +  lug  + '\n')
            lugar = Centro(nombre=lug)
            session.add(lugar)                
            session.commit()

    elif area == "autoridades superiores":    
        if "decanato" in lug:
          #agregar lugares sin tipo
          lugar = session.query(Lugar).filter_by(nombre="decanato").first() 
          if not lugar:
              print('no existe lugar, se cargara: decanato\n')
              lugar = Lugar(nombre="decanato")
              session.add(lugar)
              session.commit()

        elif "prosecr" in lug:           
            lugar = session.query(Prosecretaria).filter_by(nombre=lug).first() 
            if not lugar:
                print('no existe prosecretaria, se cargara: ' +  lug  + '\n')
                lugar = Prosecretaria(nombre=lug)
                session.add(lugar)
                session.commit()
                
        elif "secr" in lug:
            lugar = session.query(Secretaria).filter_by(nombre=lug).first() 
            if not lugar:
                print('no existe secretaria, se cargara: ' +  lug  + '\n')
                lugar = Secretaria(nombre=lug)
                session.add(lugar)                    
                session.commit()

    if lugar is None:
        print("no se definio lugar " + lug + " " + area)


    return lugar        
            
    """
    if "seminario" in func:
        lug_ = func + " " + lugar.nombre
        lugar_ = session.query(Seminario).filter_by(nombre=lug_).first()
        if not lugar_:
            lugar_ = Seminario(nombre=lug_, padre=lugar)
            session.add(lugar)
            return lugar_
    """

      
    
    
    
    
    
#verifica si existe cargo, si no existe lo crea
def setCargo(car):

    cargo = session.query(Cargo).filter_by(nombre=car).first()
    if not cargo:
        print('no existe cargo, se cargara: ' +  car  + '\n')
        cargo = Cargo(nombre=car, tipo='Docente')
        session.add(cargo)
        session.commit()  

    else:
        cargo.tipo = 'Docente'

    return cargo





def setCategorias(datos):
    ded = datos["dedicacion"].strip().lower()
    
    categorias = []
   
    #dedicacion siempre existe
    dedicacion = session.query(Categoria).filter_by(nombre=ded).first()
    if not dedicacion:
        categoria = Categoria(nombre=ded)
        categorias.append(categoria)
           
    #caracter es opcional (se define caracter en extension con el mismo que la designacion? por el momento no)           
    if 'caracter' in datos: 
        carac = datos["caracter"].strip().lower()                               
        caracter = session.query(Categoria).filter_by(nombre=carac).first()
        if not caracter:
            categoria = Categoria(nombre=carac)
            categorias.append(categoria)

    #funcion se define solo en lugar
    if(('funcion' in datos) and (datos['funcion'] is not None)):
        func = datos['funcion'].strip().lower() 
   
        if "acad" in func:
            categoria = session.query(Categoria).filter_by(nombre="academico").first()
            if not categoria:
                categoria = Categoria(nombre = "academico")   
                
        if "docente" in func:
            categoria = session.query(Categoria).filter_by(nombre="docente").first()
            if not categoria:
                categoria = Categoria(nombre = "docente")   
        
        
        elif "apoyo" in func:
            categoria = session.query(Categoria).filter_by(nombre="apoyo").first()
            if not categoria:
                categoria = Categoria(nombre = "apoyo")
        
        elif "codir" in func:
            categoria = session.query(Categoria).filter_by(nombre="codirector").first()
            if not categoria:
                categoria = Categoria(nombre = "codirector")      
        
        elif "coord" in func:
            categoria = session.query(Categoria).filter_by(nombre="coordinador").first()
            if not categoria:
                categoria = Categoria(nombre = "coordinador")

        elif "director" in func:
            categoria = session.query(Categoria).filter_by(nombre="director").first()
            if not categoria:
                categoria = Categoria(nombre = "director")          

        elif "investigador" in func:
            categoria = session.query(Categoria).filter_by(nombre="investigador").first()
            if not categoria:
                categoria = Categoria(nombre = "investigador")
                
        elif "seminario" in func:
            categoria = session.query(Categoria).filter_by(nombre="seminario").first()
            if not categoria:
                categoria = Categoria(nombre = "seminario")
        
        else:
            categoria = None
        
        if categoria is not None:
            categorias.append(categoria)
          
    return categorias
          


def setDesignacion(datos, cargo, lugar, usuario, categorias):
    id_designacion = str(datos["id_designacion"])
    old_id = "designacion" + id_designacion
    desde = datos['fecha_desde']
    hasta = datos['fecha_hasta']
    expe = datos['expediente']
    res = datos['resolucion']
   
    desde_baja = datos['fecha_baja']
    expe_baja = datos['expediente_baja']
    res_baja = datos['resolucion_baja']
        
    designacion = session.query(Designacion).filter_by(old_id=old_id).first()
    if not designacion:
        print('no existe designacion, se cargara: ' + old_id + '\n')
        designacion = Designacion(tipo='original', desde=desde, hasta=hasta, expediente=expe, resolucion=res, cargo=cargo, lugar=lugar, usuario=usuario, old_id=old_id)
        designacion.categorias = categorias
        session.add(designacion)
        session.commit()  
    
    ''' proceso la baja '''
    if desde_baja:
        old_id_baja = "baja" + old_id
        designacionBaja = session.query(Designacion).filter_by(old_id=old_id_baja).first()
        if not designacionBaja:
            print('no existe designacion de baja, se cargara: ' + old_id_baja + '\n')
            designacionBaja = Designacion(tipo='baja', desde=desde_baja, expediente=expe_baja, resolucion=res_baja, cargo=cargo, lugar=lugar, usuario=usuario, designacion_id=designacion.id, old_id=old_id_baja)
            session.add(designacionBaja)
            session.commit()  
  
  
  


      
    
    

def setExtension(datos, lugar, categorias):
    id_extension = str(datos["id_extension"])
    id_designacion = str(datos["id_designacion"])
    old_id_extension = "extension" + id_extension
    old_id_designacion = "designacion" + id_designacion
    desde = datos['fecha_desde']
    hasta = datos['fecha_hasta']
    expe = datos['expediente']
    res = datos['resolucion']
    ded = datos["dedicacion"].strip().lower()
    desde_baja = datos['fecha_baja']
    expe_baja = datos['expediente_baja']
    res_baja = datos['resolucion_baja']
        
     
   
    extension = session.query(Designacion).filter_by(old_id=old_id_extension).first()
    if not extension:
        designacion = session.query(Designacion).filter_by(old_id=old_id_designacion).first()
        if not designacion:
            print("No esta definida la designacion para agregar la extension" + old_id_designacion)
            return 
         
        usuario_id = designacion.usuario_id
        cargo_id = designacion.cargo_id
    
        
        print('no existe extension, se cargara: ' + old_id_extension + '\n')
        extension = Designacion(tipo='extension', desde=desde_baja, hasta=hasta, expediente=expe, cargo_id=cargo_id, resolucion=res, lugar=lugar, usuario_id=usuario_id, designacion_id=designacion.id, old_id=old_id_extension)
        extension.categorias = categorias
        session.add(extension)
        session.commit()  
        

        ''' proceso la baja '''
        if desde_baja:
            old_id_baja = "baja" + old_id_extension
            designacionBaja = session.query(Designacion).filter_by(old_id=old_id_baja).first()
            if not designacionBaja:
                print('no existe designacion de baja, se cargara: ' + old_id_baja + '\n')
                designacionBaja = Designacion(tipo='baja', desde=desde_baja, expediente=expe_baja, resolucion=res_baja, cargo_id=cargo_id, lugar=lugar, usuario_id=usuario_id, designacion_id=designacion.id, old_id=old_id_baja)
                session.add(designacionBaja)
                session.commit()  
      




def setProrroga(datos, oldIdDesignacion):
    id_prorroga = str(datos["id_prorroga"])
    old_id_prorroga = "prorroga" + id_prorroga

    desde = datos['fecha_desde']
    hasta = datos['fecha_hasta']
    expe = datos['expediente']
    res = datos['resolucion']

    
    prorroga = session.query(Designacion).filter_by(old_id=old_id_prorroga).first()
    if not prorroga:
        designacion = session.query(Designacion).filter_by(old_id=oldIdDesignacion).first()
        if not designacion:
            print("No esta definida la designacion para agregar prorroga" + oldIdDesignacion)
            return False
         
        usuario_id = designacion.usuario_id
        cargo_id = designacion.cargo_id
        lugar_id = designacion.lugar_id
    
        print('no existe prorroga, se cargara: ' + old_id_prorroga + '\n')
        prorroga = Designacion(tipo='prorroga', desde=desde, hasta=hasta, expediente=expe, resolucion=res, cargo_id=cargo_id, lugar_id=lugar_id, usuario_id=usuario_id, designacion_id=designacion.id, old_id=old_id_prorroga)

        session.add(prorroga)
        session.commit()  
        
    return True
            
        

def setProrrogaDeProrroga(datos, oldIdProrroga):
    id_prorroga = str(datos["id_prorroga"])
    old_id_prorroga = "prorroga" + id_prorroga

    desde = datos['fecha_desde']
    hasta = datos['fecha_hasta']
    expe = datos['expediente']
    res = datos['resolucion']

    
    prorroga = session.query(Designacion).filter_by(old_id=old_id_prorroga).first()
    if not prorroga:
        designacion = session.query(Designacion).filter_by(old_id=oldIdDesignacion).first()
        if not designacion:
            print("No esta definida la prorroga para agregar prorroga" + oldIdProrroga)
            return False
         
        usuario_id = designacion.usuario_id
        cargo_id = designacion.cargo_id
        lugar_id = designacion.lugar_id
    
        print('no existe prorroga, se cargara: ' + old_id_prorroga + '\n')
        prorroga = Designacion(tipo='prorroga', desde=desde, hasta=hasta, expediente=expe, resolucion=res, cargo_id=cargo_id, lugar_id=lugar_id, usuario_id=usuario_id, designacion_id=designacion.designacion_id, old_id=old_id_prorroga)
        
        
        session.add(prorroga)
        session.commit()  
        
    return True
            
        




if __name__ == '__main__':

    
    users = users() #consulta de todos los usuarios de profile.users (id y dni)

    logging.info('designaciones docentes\n')
    for datos in designacionesDocentes():
        usuario = setUsuario(datos, users)
        cargo = setCargo(datos["cargo"].strip().lower())
        lugar = setLugarDocente(datos)
        categorias = setCategorias(datos)
        setDesignacion(datos, cargo=cargo, lugar=lugar, usuario=usuario, categorias=categorias)    
    
    
    logging.info('designaciones lugar\n')
    for datos in designacionesLugares():
        usuario = setUsuario(datos, users)
        cargo = setCargo(datos["cargo"].strip().lower())
        lugar = setLugarTrabajo(datos)
        categorias = setCategorias(datos)
        if not lugar:
            logging.info('No se define lugar\n')

        setDesignacion(datos, cargo=cargo, lugar=lugar, usuario=usuario, categorias=categorias)    
        
    
    logging.info('extensiones docentes de designaciones docentes\n')
    for datos in extensionesDocentesDeDesignacionesDocentes():
        lugar = setLugarDocente(datos)
        categorias = setCategorias(datos)
        setExtension(datos, lugar, categorias)
        
   
    logging.info('extensiones docentes de designaciones lugares\n')
    for datos in extensionesDocentesDeDesignacionesLugares():
        lugar = setLugarDocente(datos)
        categorias = setCategorias(datos)
        setExtension(datos, lugar, categorias)
   
    logging.info('extensiones lugares de designaciones docentes\n')   
    for datos in extensionesLugaresDeDesignacionesDocentes():
        lugar = setLugarTrabajo(datos)
        categorias = setCategorias(datos)
        setExtension(datos, lugar, categorias)
        
    logging.info('extensiones lugares de designaciones docentes\n')   
    for datos in extensionesLugaresDeDesignacionesLugares():
        lugar = setLugarTrabajo(datos)
        categorias = setCategorias(datos)
        setExtension(datos, lugar, categorias)
        
     
    logging.info('prorrogas iniciales de designacion\n')   
    for datos in prorrogasIniciales("des"):
        id = str(datos["id_designacion"])
        oldIdDesignacion = "designacion" + id
        setProrroga(datos, oldIdDesignacion)

    logging.info('prorrogas iniciales de extension\n')   
    for datos in prorrogasIniciales("ext"):
        id = str(datos["id_designacion"])
        oldIdDesignacion = "extension" + id
        setProrroga(datos, oldIdDesignacion)
        
                
    logging.info('prorrogas iniciales de prorroga\n')   
    idsProrrogas = []
    for datos in prorrogasIniciales("pro"):  
        id = str(datos["id_designacion"])
        oldIdDesignacion = "prorroga" + id
        result = setProrrogaDeProrroga(datos, oldIdDesignacion)

        if result == False:         
          idsProrrogas.append(datos["id_prorroga"])

    cantidad = 0
    if len(idsProrrogas) > 0:
        while True:
            logging.info("prorrogas restantes")         

            for datos in prorrogasDeIds(idsProrrogas):
                idsProrrogas = []
                id = str(datos["id_designacion"])
                oldIdDesignacion = "prorroga" + id
                result = setProrrogaDeProrroga(datos, oldIdDesignacion)
                if result == False:         
                   idsProrrogas.append(datos["id_prorroga"])
           
                if cantidad == len(idsProrrogas):
                    break;
                    
                cantidad = len(idProrrogas)
        
    logging.info("no se procesan mas prorrogas, quedaron sin cargar " + str(cantidad))   
        
        

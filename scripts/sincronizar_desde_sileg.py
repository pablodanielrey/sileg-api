import psycopg2
from psycopg2.extras import DictCursor
import os
import uuid
import datetime
import logging
logging.getLogger().setLevel(logging.DEBUG)

"""
utndocentes=> \d designacion_docente
                                                 Tabla «public.designacion_docente»
         Columna         |          Tipo          |                                  Modificadores                                   
-------------------------+------------------------+----------------------------------------------------------------------------------
 desig_id                | integer                | not null valor por omisión nextval('designacion_docente_desig_id_seq'::regclass)
 desig_tipocargo_id      | integer                | not null
 desig_empleado_id       | integer                | not null
 desig_tipocaracter_id   | integer                | not null
 desig_tipodedicacion_id | integer                | not null
 desig_fecha_desde       | date                   | not null
 desig_fecha_hasta       | date                   | 
 desig_tipoextraord_id   | integer                | 
 desig_tipofincargo_id   | integer                | 
 desig_fecha_baja        | date                   | 
 desig_tipobaja_id       | integer                |                                                                                                                                                                                          
 desig_prorrogada_con    | integer                |                                                                                                                                                                                          
 desig_observaciones     | character varying(255) |                                                                                                                                                                                          
 desig_resolucionalta_id | integer                | not null                                                                                                                                                                                 
 desig_resolucionbaja_id | integer                |                                                                                                                                                                                          
 desig_catxmat_id        | integer                |                                                                                                                                                                                          
 desig_lugdetrab_id      | integer                |                                                                                                                                                                                          
 desig_funcion_id        | integer                |                                                                                                                                                                                          
 desig_comision          | character varying(20)  |                                                                                                                                                                                          
 desig_reempa            | integer                |                                                                                                                                                                                          
 desig_ord_esajust       | bit(1)                 |                                                                                                                                                                                          
 desig_ord_fdesde        | date                   |                                                                                                                                                                                          
 desig_ord_fhasta        | date                   |                                                                                                                                                                                          
 desig_convalidado       | date                   |                                                                                                                                                                                          
 desig_resolucionord_id  | integer                |                                                                                                                                                                                          
 usuario_log             | integer                |                                                                                                                                                                                          
Índices:                                                                                                                                                                                                                                     
    "designacion_docente_pkey" PRIMARY KEY, btree (desig_id)                                                                                                                                                                                 
Restricciones de llave foránea:                                                                                                                                                                                                              
    "designacion_docente_desig_catxmat_id_fkey" FOREIGN KEY (desig_catxmat_id) REFERENCES catedras_x_materia(catxmat_id)                                                                                                                     
    "designacion_docente_desig_empleado_id_fkey" FOREIGN KEY (desig_empleado_id) REFERENCES empleado(empleado_id)                                                                                                                            
    "designacion_docente_desig_funcion_id_fkey" FOREIGN KEY (desig_funcion_id) REFERENCES funcion(funcion_id)                                                                                                                                
    "designacion_docente_desig_lugdetrab_id_fkey" FOREIGN KEY (desig_lugdetrab_id) REFERENCES lugar_de_trabajo(lugdetrab_id)                                                                                                                 
    "designacion_docente_desig_prorrogada_con_fkey" FOREIGN KEY (desig_prorrogada_con) REFERENCES prorroga(prorroga_id)                                                                                                                      
    "designacion_docente_desig_reempa_fkey" FOREIGN KEY (desig_reempa) REFERENCES designacion_docente(desig_id)
    "designacion_docente_desig_resolucionalta_id_fkey" FOREIGN KEY (desig_resolucionalta_id) REFERENCES resolucion(resolucion_id)
    "designacion_docente_desig_resolucionbaja_id_fkey" FOREIGN KEY (desig_resolucionbaja_id) REFERENCES resolucion(resolucion_id)
    "designacion_docente_desig_resolucionord_id_fkey" FOREIGN KEY (desig_resolucionord_id) REFERENCES resolucion(resolucion_id)
    "designacion_docente_desig_tipobaja_id_fkey" FOREIGN KEY (desig_tipobaja_id) REFERENCES tipo_baja(tipobajadesig_id)
    "designacion_docente_desig_tipocaracter_id_fkey" FOREIGN KEY (desig_tipocaracter_id) REFERENCES tipo_caracter(tipocaracter_id)
    "designacion_docente_desig_tipocargo_id_fkey" FOREIGN KEY (desig_tipocargo_id) REFERENCES tipo_cargo(tipocargo_id)
    "designacion_docente_desig_tipodedicacion_id_fkey" FOREIGN KEY (desig_tipodedicacion_id) REFERENCES tipo_dedicacion(tipodedicacion_id)
    "designacion_docente_desig_tipoextraord_id_fkey" FOREIGN KEY (desig_tipoextraord_id) REFERENCES tipo_caracter_extraordinario(tipoextraord_id)
    "designacion_docente_desig_tipofincargo_id_fkey" FOREIGN KEY (desig_tipofincargo_id) REFERENCES tipo_fin_cargo(tipofincargo_id)
Referenciada por:
    TABLE "designacion_docente" CONSTRAINT "designacion_docente_desig_reempa_fkey" FOREIGN KEY (desig_reempa) REFERENCES designacion_docente(desig_id)
    TABLE "extension" CONSTRAINT "extension_extension_designacion_id_fkey" FOREIGN KEY (extension_designacion_id) REFERENCES designacion_docente(desig_id)
    TABLE "licencia" CONSTRAINT "licencia_licencia_designacion_id_fkey" FOREIGN KEY (licencia_designacion_id) REFERENCES designacion_docente(desig_id)
Triggers:
    designacion_docente_log AFTER DELETE OR UPDATE ON designacion_docente FOR EACH ROW EXECUTE PROCEDURE process_designacion_docente_log()



utndocentes=> \d empleado
                                                    Tabla «public.empleado»
          Columna           |         Tipo          |                              Modificadores                               
----------------------------+-----------------------+--------------------------------------------------------------------------
 empleado_id                | integer               | not null valor por omisión nextval('empleado_empleado_id_seq'::regclass)
 empleado_pers_id           | integer               | not null
 empleado_cuil              | character varying(13) | 
 empleado_estadocivil_id    | integer               | 
 empleado_domicilio_calle   | character varying(50) | 
 empleado_domicilio_nro     | character varying(10) | 
 empleado_domicilio_piso    | character varying(50) | 
 empleado_domicilio_dpto    | character varying(50) | 
 empleado_domicilio_loca_id | integer               | 
 empleado_fechaingreso_unlp | date                  | 
 empleado_nro_cuenta        | character varying(50) | 
 empleado_cobraen_suc_id    | integer               | 
 empleado_osocial_id        | integer               | 
 empleado_segvida_id        | integer               | 
 empleado_fecha_jubilacion  | date                  | 
 empleado_segvida_oblig     | bit(1)                | 
 empleado_segvida_banco_id  | integer               | 
 empleado_segvida_polnum1   | character varying(20) | 
 empleado_segvida_polnum2   | character varying(20) | 
 empleado_segvida_polnum3   | character varying(20) | 
 usuario_log                | integer               | 
Índices:
    "empleado_pkey" PRIMARY KEY, btree (empleado_id)
Restricciones de llave foránea:
    "empleado_empleado_cobraen_suc_id_fkey" FOREIGN KEY (empleado_cobraen_suc_id) REFERENCES sucursal_banco(sucursal_id)
    "empleado_empleado_domicilio_loca_id_fkey" FOREIGN KEY (empleado_domicilio_loca_id) REFERENCES localidad(loca_id)
    "empleado_empleado_estadocivil_id_fkey" FOREIGN KEY (empleado_estadocivil_id) REFERENCES tipo_estado_civil(tipoestcivil_id)
    "empleado_empleado_osocial_id_fkey" FOREIGN KEY (empleado_osocial_id) REFERENCES obra_social(osocial_id)
    "empleado_empleado_pers_id_fkey" FOREIGN KEY (empleado_pers_id) REFERENCES persona(pers_id)
    "empleado_empleado_segvida_id_fkey" FOREIGN KEY (empleado_segvida_id) REFERENCES seguro_de_vida(segvida_id)
Referenciada por:
    TABLE "antiguedad" CONSTRAINT "antiguedad_ant_emp_id_fkey" FOREIGN KEY (ant_emp_id) REFERENCES empleado(empleado_id)
    TABLE "cert_jub" CONSTRAINT "cert_jub_cert_jub_idemp_fkey" FOREIGN KEY (cert_jub_idemp) REFERENCES empleado(empleado_id)
    TABLE "designacion_docente" CONSTRAINT "designacion_docente_desig_empleado_id_fkey" FOREIGN KEY (desig_empleado_id) REFERENCES empleado(empleado_id)
    TABLE "email" CONSTRAINT "email_email_empleado_id_fkey" FOREIGN KEY (email_empleado_id) REFERENCES empleado(empleado_id)
    TABLE "familiar_a_cargo" CONSTRAINT "familiar_a_cargo_familiarcargo_empleado_id_fkey" FOREIGN KEY (familiarcargo_empleado_id) REFERENCES empleado(empleado_id)
    TABLE "prorroga" CONSTRAINT "prorroga_prorroga_idemp_fkey" FOREIGN KEY (prorroga_idemp) REFERENCES empleado(empleado_id)
    TABLE "telefono" CONSTRAINT "telefono_telef_empleado_id_fkey" FOREIGN KEY (telef_empleado_id) REFERENCES empleado(empleado_id)
    TABLE "titulo_grado_empleado" CONSTRAINT "titulo_grado_empleado_titgrademp_empleado_id_fkey" FOREIGN KEY (titgrademp_empleado_id) REFERENCES empleado(empleado_id)
    TABLE "titulo_por_empleado" CONSTRAINT "titulo_por_empleado_titempleado_empleado_id_fkey" FOREIGN KEY (titempleado_empleado_id) REFERENCES empleado(empleado_id)
    TABLE "titulo_postgrado_empleado" CONSTRAINT "titulo_postgrado_empleado_titposemp_empleado_id_fkey" FOREIGN KEY (titposemp_empleado_id) REFERENCES empleado(empleado_id)
Triggers:
    empleado_log AFTER DELETE OR UPDATE ON empleado FOR EACH ROW EXECUTE PROCEDURE process_empleado_log()


"""

"""
                  id                  |           creado           |        actualizado         |             nombre              |    tipo    | descripcion 
--------------------------------------+----------------------------+----------------------------+---------------------------------+------------+-------------
 245eae51-28c4-4c6b-9085-354606399666 | 2017-10-24 18:28:53.449819 |                            | Cumple Funciones                | No Docente | 
 dbf391cd-1212-4e40-a795-f466b0c2406d | 2017-07-19 12:14:51.557046 | 2018-11-22 17:27:04.385892 | Ayudante Diplomado D/S          | Docente    | 
 ca0c7105-ade2-4fab-b14c-086248b7a447 | 2017-07-19 12:14:51.823542 | 2018-11-22 17:27:04.511969 | Titular D/S                     | Docente    | 
 750780c1-496a-4ca9-bcb7-9b3835f205c1 | 2017-07-19 12:15:06.264827 | 2018-11-22 17:27:04.562693 | Ayudante Alumno D/S             | Docente    | 
 718e8e33-2989-4337-8d79-2609268d315e | 2017-07-19 12:14:51.241525 | 2018-11-22 17:27:04.76296  | Jefe de Auxiliares Docentes D/S | Docente    | 
 b65f8e8b-80ee-4ff8-9bf2-f04ba2bdd397 | 2017-07-19 12:14:52.148218 | 2018-11-22 17:27:04.895404 | Adjunto D/S                     | Docente    | 
 6f0c238b-808c-4692-ac26-aaccf3d22cb1 | 2017-07-19 12:16:25.439283 | 2018-11-22 17:27:04.945535 | Asociado D/S                    | Docente    | 
 07bac038-f4a8-437b-843e-607ea89b72e2 | 2018-11-22 17:28:19.384737 |                            | Cumple Funciones                | Docente    | 
 99528020-6389-4d8e-a88d-5629b6b4cac0 | 2018-11-22 17:28:19.477904 |                            | Jefe de Trabajos Prácticos D/S  | Docente    | 
 28b3a978-15ad-4c17-9421-c1fd75ee01ef | 2017-07-19 12:19:54.620539 | 2018-11-22 17:30:50.874862 | Vicedecano                      | Autoridad  | 
 06adf7ed-51a9-4774-8606-0f46a69fbadf | 2017-07-19 12:20:01.861184 | 2018-11-22 17:30:50.942422 | Decano                          | Autoridad  | 
 325e5e55-375b-4768-9e7b-c14de0a85553 | 2017-07-19 12:19:44.286407 | 2018-11-22 17:30:50.995948 | Secretario                      | Autoridad  | 
 84a2bc10-f82d-489b-962c-1a8f25bd1796 | 2017-07-19 12:19:46.103019 | 2018-11-22 17:30:51.036889 | Pro Secretario                  | Autoridad  | 


utndocentes=> select * from tipo_cargo;
 tipocargo_id |      tipocargo_nombre       | tipocargo_abrev | tipocargo_orden | usuario_log 
--------------+-----------------------------+-----------------+-----------------+-------------
            9 | Titular                     | TIT             |               5 |            
            2 | Asociado                    | ASOC            |               6 |            
            3 | Adjunto                     | ADJ             |               7 |            
           16 | Decano                      | Dec.            |               1 |            
           17 | Vicedecano                  | Viced.          |               2 |           6
           18 | Secretario                  | Secr.           |               3 |           6
           20 | Prosecretario               | Prosec.         |               4 |           6
            5 | Ayudante Diplomado          | A/D             |               9 |          47
            6 | Ayudante Alumno             | A/A             |              10 |          47
            4 | Jefe de Auxiliares Docentes | JAD             |               8 |          47
           21 | ...                         | .               |               0 |          47
(11 filas)

utndocentes=> select * from tipo_dedicacion;
 tipodedicacion_id | tipodedicacion_nombre | tipodedicacion_factaextender | tipodedicacion_abrev | usuario_log 
-------------------+-----------------------+------------------------------+----------------------+-------------
                 3 | Exclusiva             | 0                            | D/E                  |            
                 2 | Semi Exclusiva        | 0                            | S/D                  |            
                 7 | Simple                | 1                            | D/S                  |            
                 8 | Tiempo completo       | 0                            | T.comp.              |           6
                 9 | Semidedicación        | 1                            | S/D                  |          40
                11 | A-H                   | 1                            | A-H                  |          40
                12 | ...                   | 0                            | .                    |          47
(7 filas)


utndocentes=> select distinct(desig_tipodedicacion_id), desig_tipocargo_id, concat(c.tipocargo_nombre,' ', tipodedicacion_abrev) as fullname 
from designacion_docente d inner join tipo_cargo c on (c.tipocargo_id = d.desig_tipocargo_id) 
inner join tipo_dedicacion de on (d.desig_tipodedicacion_id = de.tipodedicacion_id) order by desig_tipocargo_id;

 desig_tipodedicacion_id | desig_tipocargo_id |            fullname             
-------------------------+--------------------+---------------------------------
                       2 |                  2 | Asociado S/D
                       3 |                  2 | Asociado D/E
                       7 |                  2 | Asociado D/S
                       2 |                  3 | Adjunto S/D
                       3 |                  3 | Adjunto D/E
                       7 |                  3 | Adjunto D/S
                       9 |                  3 | Adjunto S/D
                      11 |                  3 | Adjunto A-H
                      12 |                  3 | Adjunto .
                       2 |                  4 | Jefe de Auxiliares Docentes S/D
                       3 |                  4 | Jefe de Auxiliares Docentes D/E
                       7 |                  4 | Jefe de Auxiliares Docentes D/S
                       9 |                  4 | Jefe de Auxiliares Docentes S/D
                       2 |                  5 | Ayudante Diplomado S/D
                       3 |                  5 | Ayudante Diplomado D/E
                       7 |                  5 | Ayudante Diplomado D/S
                       9 |                  5 | Ayudante Diplomado S/D
                      11 |                  5 | Ayudante Diplomado A-H
                      12 |                  5 | Ayudante Diplomado .
                       7 |                  6 | Ayudante Alumno D/S
                       2 |                  9 | Titular S/D
                       3 |                  9 | Titular D/E
                       7 |                  9 | Titular D/S
                       9 |                  9 | Titular S/D
                      11 |                  9 | Titular A-H
                       3 |                 16 | Decano D/E
                       3 |                 17 | Vicedecano D/E
                       7 |                 17 | Vicedecano D/S
                       3 |                 18 | Secretario D/E
                       7 |                 18 | Secretario D/S
                       8 |                 18 | Secretario T.comp.
                      11 |                 18 | Secretario A-H
                       3 |                 20 | Prosecretario D/E
                       8 |                 20 | Prosecretario T.comp.
                       3 |                 21 | ... D/E
                      11 |                 21 | ... A-H
                      12 |                 21 | ... .
"""


def obtener_prorroga(prorroga_id, cur):
    cur.execute("""
        SELECT prorroga_id, prorroga_fecha_desde, prorroga_fecha_hasta, prorroga_prorrogada_con
        FROM prorroga
        WHERE prorroga_id = %s
        ORDER BY 
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

def importar_designacion(d, cur):
    logging.info("Importando designacion: {}".format(d))
    id = d["desig_id"]

    if d["desig_tipobaja_id"]:
        logging.info("Crear designaciones de baja")

    prorrogas = []
    if d["desig_prorrogada_con"]:
        prorrogas = obtener_prorrogas_de(d["desig_prorrogada_con"], cur)
        for p in prorrogas:
            logging.info("Crear prorroga: {}".format(p))

    
    extensiones = obtener_extensiones(id, cur)
    for e in extensiones:
        if e["extension_prorrogada_con"]:
            prorrogas_ext = obtener_prorrogas_de(d["extension_prorrogada_con"], cur)
            logging.info("Creo extension: {}".format(e))
            for ep in prorrogas_ext:
                logging.info("Creo extension prorroga {}".format(ep))


if __name__ == '__main__':
    conn = psycopg2.connect("host='{}' user='{}' password='{}' dbname={}".format(
        os.environ['OLD_SILEG_DB_HOST'],
        os.environ['OLD_SILEG_DB_USER'],
        os.environ['OLD_SILEG_DB_PASSWORD'],
        os.environ['OLD_SILEG_DB_NAME']
    ))
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("SELECT * FROM designacion_docente where desig_id =  208")
        for d in cur:
            importar_designacion(d, cur)


    finally:
        cur.close()
        conn.close()        

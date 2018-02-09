import psycopg2
from psycopg2.extras import DictCursor
import os
import uuid
import datetime
import logging
logging.getLogger().setLevel(logging.DEBUG)

"""
    hay que sincronizar:

                   Table "sileg.cargo"
   Column    |            Type             |   Modifiers
-------------+-----------------------------+---------------
 id          | character varying           | not null
 creado      | timestamp without time zone | default now()
 actualizado | timestamp without time zone |
 nombre      | character varying           |
 tipo        | character varying           |
Indexes:
    "cargo_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "sileg.designacion" CONSTRAINT "designacion_cargo_id_fkey" FOREIGN KEY (cargo_id) REFERENCES sileg.cargo(id)

        Index "sileg.cargo_pkey"
 Column |       Type        | Definition
--------+-------------------+------------
 id     | character varying | id
primary key, btree, for table "sileg.cargo"

           Table "sileg.catedra"
   Column   |       Type        | Modifiers
------------+-------------------+-----------
 id         | character varying | not null
 materia_id | character varying |
Indexes:
    "catedra_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "catedra_id_fkey" FOREIGN KEY (id) REFERENCES sileg.lugar(id)

       Index "sileg.catedra_pkey"
 Column |       Type        | Definition
--------+-------------------+------------
 id     | character varying | id
primary key, btree, for table "sileg.catedra"

                  Table "sileg.categoria"
   Column    |            Type             |   Modifiers
-------------+-----------------------------+---------------
 id          | character varying           | not null
 creado      | timestamp without time zone | default now()
 actualizado | timestamp without time zone |
 nombre      | character varying           |
Indexes:
    "categoria_pkey" PRIMARY KEY, btree (id)
    "categoria_nombre_key" UNIQUE CONSTRAINT, btree (nombre)
Referenced by:
    TABLE "sileg.categoria_designacion" CONSTRAINT "categoria_designacion_categoria_id_fkey" FOREIGN KEY (categoria_id) REFERENCES sileg.categoria(id)

      Table "sileg.categoria_designacion"
     Column     |       Type        | Modifiers
----------------+-------------------+-----------
 designacion_id | character varying |
 categoria_id   | character varying |
Foreign-key constraints:
    "categoria_designacion_categoria_id_fkey" FOREIGN KEY (categoria_id) REFERENCES sileg.categoria(id)
    "categoria_designacion_designacion_id_fkey" FOREIGN KEY (designacion_id) REFERENCES sileg.designacion(id)

   Index "sileg.categoria_nombre_key"
 Column |       Type        | Definition
--------+-------------------+------------
 nombre | character varying | nombre
unique, btree, for table "sileg.categoria"

      Index "sileg.categoria_pkey"
 Column |       Type        | Definition
--------+-------------------+------------
 id     | character varying | id
primary key, btree, for table "sileg.categoria"

                  Table "sileg.designacion"
     Column     |            Type             |   Modifiers
----------------+-----------------------------+---------------
 id             | character varying           | not null
 creado         | timestamp without time zone | default now()
 actualizado    | timestamp without time zone |
 desde          | date                        |
 hasta          | date                        |
 historico      | boolean                     |
 expediente     | character varying           |
 resolucion     | character varying           |
 tipo           | character varying           |
 designacion_id | character varying           |
 usuario_id     | character varying           |
 cargo_id       | character varying           |
 lugar_id       | character varying           |
 old_id         | character varying           |
Indexes:
    "designacion_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "designacion_cargo_id_fkey" FOREIGN KEY (cargo_id) REFERENCES sileg.cargo(id)
    "designacion_designacion_id_fkey" FOREIGN KEY (designacion_id) REFERENCES sileg.designacion(id)
    "designacion_lugar_id_fkey" FOREIGN KEY (lugar_id) REFERENCES sileg.lugar(id)
    "designacion_usuario_id_fkey" FOREIGN KEY (usuario_id) REFERENCES sileg.usuario(id)
Referenced by:
    TABLE "sileg.categoria_designacion" CONSTRAINT "categoria_designacion_designacion_id_fkey" FOREIGN KEY (designacion_id) REFERENCES sileg.designacion(id)
    TABLE "sileg.designacion" CONSTRAINT "designacion_designacion_id_fkey" FOREIGN KEY (designacion_id) REFERENCES sileg.designacion(id)

     Index "sileg.designacion_pkey"
 Column |       Type        | Definition
--------+-------------------+------------
 id     | character varying | id
primary key, btree, for table "sileg.designacion"

                    Table "sileg.lugar"
   Column    |            Type             |   Modifiers
-------------+-----------------------------+---------------
 id          | character varying           | not null
 creado      | timestamp without time zone | default now()
 actualizado | timestamp without time zone |
 nombre      | character varying           |
 tipo        | character varying           |
 padre_id    | character varying           |
 cambio_id   | character varying           |
Indexes:
    "lugar_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "lugar_cambio_id_fkey" FOREIGN KEY (cambio_id) REFERENCES sileg.lugar(id)
    "lugar_padre_id_fkey" FOREIGN KEY (padre_id) REFERENCES sileg.lugar(id)
Referenced by:
    TABLE "sileg.catedra" CONSTRAINT "catedra_id_fkey" FOREIGN KEY (id) REFERENCES sileg.lugar(id)
    TABLE "sileg.designacion" CONSTRAINT "designacion_lugar_id_fkey" FOREIGN KEY (lugar_id) REFERENCES sileg.lugar(id)
    TABLE "sileg.lugar" CONSTRAINT "lugar_cambio_id_fkey" FOREIGN KEY (cambio_id) REFERENCES sileg.lugar(id)
    TABLE "sileg.lugar" CONSTRAINT "lugar_padre_id_fkey" FOREIGN KEY (padre_id) REFERENCES sileg.lugar(id)

        Index "sileg.lugar_pkey"
 Column |       Type        | Definition
--------+-------------------+------------
 id     | character varying | id
primary key, btree, for table "sileg.lugar"

                   Table "sileg.materia"
   Column    |            Type             |   Modifiers
-------------+-----------------------------+---------------
 id          | character varying           | not null
 creado      | timestamp without time zone | default now()
 actualizado | timestamp without time zone |
 nombre      | character varying           |
Indexes:
    "materia_pkey" PRIMARY KEY, btree (id)

       Index "sileg.materia_pkey"
 Column |       Type        | Definition
--------+-------------------+------------
 id     | character varying | id
primary key, btree, for table "sileg.materia"

                   Table "sileg.usuario"
   Column    |            Type             |   Modifiers
-------------+-----------------------------+---------------
 id          | character varying           | not null
 creado      | timestamp without time zone | default now()
 actualizado | timestamp without time zone |
Indexes:
    "usuario_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "sileg.designacion" CONSTRAINT "designacion_usuario_id_fkey" FOREIGN KEY (usuario_id) REFERENCES sileg.usuario(id)

       Index "sileg.usuario_pkey"
 Column |       Type        | Definition
--------+-------------------+------------
 id     | character varying | id
primary key, btree, for table "sileg.usuario"



    hacia estas tablas:

sileg=# \dt
               List of relations
 Schema |         Name          | Type  | Owner
--------+-----------------------+-------+-------
 public | cargo                 | table | sileg
 public | catedra               | table | sileg
 public | categoria             | table | sileg
 public | categoria_designacion | table | sileg
 public | designacion           | table | sileg
 public | lugar                 | table | sileg
 public | materia               | table | sileg
 public | usuario               | table | sileg

"""

if __name__ == '__main__':
    conn = psycopg2.connect("host='{}' user='{}' password='{}' dbname={}".format(
        os.environ['SILEG_DB_HOST'],
        os.environ['SILEG_DB_USER'],
        os.environ['SILEG_DB_PASSWORD'],
        os.environ['SILEG_DB_NAME']
    ))
    cur = conn.cursor()
    try:
        conn2 = psycopg2.connect("host='{}' user='{}' password='{}' dbname={}".format(
            os.environ['OLD_SILEG_DB_HOST'],
            os.environ['OLD_SILEG_DB_USER'],
            os.environ['OLD_SILEG_DB_PASSWORD'],
            os.environ['OLD_SILEG_DB_NAME']
        ))
        cur2 = conn2.cursor(cursor_factory=DictCursor)
        try:
            ''' sinc usuarios '''
            cur2.execute('select id, creado, actualizado from sileg.usuario')
            for u in cur2.fetchall():
                logging.info('sincronizando: {}'.format(u))
                try:
                    cur.execute('select id from usuario where id = %(id)s', u)
                    if cur.rowcount <= 0:
                        logging.info('insertando usuario')
                        cur.execute('insert into usuario (id, creado, actualizado) values (%(id)s,%(creado)s,%(actualizado)s)', u)
                        conn.commit()
                    else:
                        logging.info('el usuario ya existe')

                except Exception as e:
                    logging.exception(e)
                    conn.rollback()

            ''' sinc cargo '''
            cur2.execute('select id, creado, actualizado, nombre, tipo from sileg.cargo')
            for c in cur2.fetchall():
                logging.info('sincronizando: {}'.format(c))
                try:
                    cur.execute('select id from cargo where id = %(id)s', c)
                    if cur.rowcount <= 0:
                        logging.info('insertando cargo')
                        cur.execute('insert into cargo (id, creado, actualizado, nombre, tipo) values (%(id)s,%(creado)s,%(actualizado)s,%(nombre)s,%(tipo)s)', c)
                        conn.commit()
                    else:
                        logging.info('el cargo ya existe')

                except Exception as e:
                    logging.exception(e)
                    conn.rollback()

            ''' sinc categoria '''
            cur2.execute('select id, creado, actualizado, nombre from sileg.categoria')
            for c in cur2.fetchall():
                logging.info('sincronizando: {}'.format(c))
                try:
                    cur.execute('select id from categoria where id = %(id)s', c)
                    if cur.rowcount <= 0:
                        logging.info('insertando categoria')
                        cur.execute('insert into categoria (id, creado, actualizado, nombre) values (%(id)s,%(creado)s,%(actualizado)s,%(nombre)s)', c)
                        conn.commit()
                    else:
                        logging.info('la categoria ya existe')

                except Exception as e:
                    logging.exception(e)
                    conn.rollback()

            ''' sinc lugar '''
            cur2.execute('select id, creado, actualizado, nombre, tipo, padre_id, cambio_id from sileg.lugar')
            for l in cur2.fetchall():
                logging.info('sincronizando: {}'.format(l))
                try:
                    cur.execute('select id, creado, actualizado, nombre, tipo, padre_id, cambio_id from lugar where id = %(id)s', l)
                    if cur.rowcount <= 0:
                        logging.info('insertando lugar')
                        cur.execute('insert into lugar (id, creado, actualizado, nombre, tipo, padre_id, cambio_id) values (%(id)s,%(creado)s,%(actualizado)s,%(nombre)s,%(tipo)s,%(padre_id)s,%(cambio_id)s)', l)
                        conn.commit()
                    else:
                        logging.info('el lugar ya existe')

                except Exception as e:
                    logging.exception(e)
                    conn.rollback()

            ''' sinc materia '''
            cur2.execute('select id, creado, actualizado, nombre from sileg.materia')
            for l in cur2.fetchall():
                logging.info('sincronizando: {}'.format(l))
                try:
                    cur.execute('select id, creado, actualizado, nombre from materia where id = %(id)s', l)
                    if cur.rowcount <= 0:
                        logging.info('insertando materia')
                        cur.execute('insert into materia (id, creado, actualizado, nombre) values (%(id)s,%(creado)s,%(actualizado)s,%(nombre)s)', l)
                        conn.commit()
                    else:
                        logging.info('la materia ya existe')

                except Exception as e:
                    logging.exception(e)
                    conn.rollback()

            ''' sinc catedra '''
            cur2.execute('select id, materia_id from sileg.catedra')
            for c in cur2.fetchall():
                logging.info('sincronizando: {}'.format(c))
                try:
                    cur.execute('select id, materia_id from catedra where id = %(id)s', c)
                    if cur.rowcount <= 0:
                        logging.info('insertando catedra')
                        cur.execute('insert into catedra (id, materia_id) values (%(id)s,%(materia_id)s)', c)
                        conn.commit()
                    else:
                        logging.info('la catedra ya existe')

                except Exception as e:
                    logging.exception(e)
                    conn.rollback()

            ''' sinc designacion '''
            cur2.execute('select id, creado, actualizado, desde, hasta, historico, expediente, resolucion, tipo, designacion_id, usuario_id, cargo_id, lugar_id, old_id from sileg.designacion')
            for d in cur2.fetchall():
                logging.info('sincronizando: {}'.format(d))
                try:
                    cur.execute('select id from designacion where id = %(id)s', d)
                    if cur.rowcount <= 0:
                        logging.info('insertando designacion')
                        cur.execute("""insert into designacion (id,creado,actualizado,desde,hasta,historico,expediente,resolucion,tipo,designacion_id,usuario_id,cargo_id,lugar_id,old_id) \
                                    values (%(id)s,%(creado)s,%(actualizado)s,%(desde)s,%(hasta)s,%(historico)s,%(expediente)s,%(resolucion)s,%(tipo)s,%(designacion_id)s,%(usuario_id)s,%(cargo_id)s,%(lugar_id)s,%(old_id)s)""", d)
                        conn.commit()
                    else:
                        logging.info('la designacion ya existe')

                except Exception as e:
                    logging.exception(e)
                    conn.rollback()

            ''' sinc categoria designacion '''
            cur2.execute('select designacion_id, categoria_id from sileg.categoria_designacion')
            for c in cur2.fetchall():
                logging.info('sincronizando: {}'.format(c))
                try:
                    cur.execute('select designacion_id, categoria_id from categoria_designacion where designacion_id = %(designacion_id)s and categoria_id = %(categoria_id)s', c)
                    if cur.rowcount <= 0:
                        logging.info('insertando categoria designacion')
                        cur.execute('insert into categoria_designacion (designacion_id, categoria_id) values (%(designacion_id)s,%(categoria_id)s)', c)
                        conn.commit()
                    else:
                        logging.info('la categoria_designacion ya existe')

                except Exception as e:
                    logging.exception(e)
                    conn.rollback()
        finally:
            cur2.close()
            conn2.close()

    finally:
        cur.close()
        conn.close()

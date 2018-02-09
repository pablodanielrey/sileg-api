import logging
logging.getLogger().setLevel(logging.DEBUG)

import sys
import os
import psycopg2

if __name__ == '__main__':


    host = os.environ['SILEG_DB_HOST']
    user = os.environ['SILEG_DB_USER']
    passwd = os.environ['SILEG_DB_PASSWORD']
    base = os.environ['SILEG_DB_NAME']

    con = psycopg2.connect(host=host, user=user, password=passwd, database=base)

    # COPY(select dni, lastname, name  from (select distinct(user_id) from assistance.schedules) as s inner join profile.users u on (u.id = s.user_id) order by lastname, name) TO '/tmp/users.csv' DELIMITER ',' CSV HEADER;

    try:
        cur = con.cursor()
        try:
            with open('/tmp/usuarios.csv','w') as f2:
                cur.execute("""
                    SELECT distinct(dni), lastname, name
                    FROM assistance.attlog  a inner join profile.users u on (u.id = a.user_id)
                    WHERE log > '2017-01-01' order by lastname, name;
                """);
                usuarios = cur.fetchall()
                for u in usuarios:
                    dni = u[0]
                    lastname = u[1]
                    name = u[2]
                    cur.execute("""
                       SELECT u.name, u.lastname, o.id, o.name, d.sstart, d.send, o.type, o.assistance
                       FROM profile.users u inner join designations.designations d on (u.id = d.User_id) inner join offices.offices o on (o.id = d.office_id)
                       WHERE dni = %s and send is  null and assistance
                    """,(dni, ));

                    datos = cur.fetchall()
                    if len(datos) <= 0:
                        f2.write('{},{},{},{},{}\n'.format(dni, lastname, name, 'No posee',''))

                    else:
                        for d in datos:
                            f2.write('{},{},{},{},{}\n'.format(dni, lastname, name, d[3],d[2]))

        except Exception as e:
            print (e)
        finally:
            cur.close()

    finally:
        con.close()

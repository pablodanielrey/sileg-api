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
            with open('usuarios.csv','r') as f, open('usuarios2.csv','w') as f2:
                for line in f:
                    row = line.split(',')
                    dni = row[0]

                    print(dni)
                    cur.execute("""
                       SELECT id
                       FROM profile.users
                       WHERE dni = %s
                    """,(dni, ));

                    id = cur.fetchone()[0]
                    f2.write(id + ',' + line)

        except Exception as e:
            print (e)
        finally:
            cur.close()

    finally:
        con.close()

import sys
import csv
import re
import logging
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == '__main__':

    #from sileg.model import obtener_session
    #from sileg.model.entities import Cargo

    reg = re.compile('[A|B|C|D|E]+.*')
    
    archivo = sys.argv[1]
    with open(archivo,'r') as f:
        c = csv.reader(f, delimiter=',', quotechar="\"")
        for r in c:
            cargo = r[7].strip()

            if cargo == 'Clase Grupo':
                continue

            dni = r[1].strip().lower()
            n = r[2].split(',')
            nombre = ''
            apellido = ''
            if len(n) >= 2:
                nombre = n[0].strip().capitalize()
                apellido = n[1].strip().capitalize()
            else:
                nombre = n[0].strip().capitalize()

            r = {
                'cargo': cargo,
                'dni': dni,
                'nombre': nombre,
                'apellido': apellido
            }
            
            m = reg.match(cargo)
            if m:
                # es no docente
                logging.debug(r)

    """
    with obtener_session() as s:
        for c in cargos:
            c1 = s.query(Cargo).filter(Cargo.id == c.id).one_or_none()
            if c1:
                c1.nombre = c.nombre
                c1.tipo = c.tipo
            else:
                s.add(c)
            s.commit()    
    """
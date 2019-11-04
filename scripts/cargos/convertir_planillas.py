
import sys
import os
from os.path import isfile
import re
import logging
logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':

    d = sys.argv[1]
    check = re.compile('ALFA.*?(\d\d)(\d\d)\.txt')
    archivos = [f for f in os.listdir(d) if check.match(f)]
    
    """ genero la estructura de meses y años para poder cargar los cargos indicados """
    cargos = {}
    for a in archivos:
        grupos = check.match(a)
        mes = grupos.group(1)
        ano = grupos.group(2)
        if ano not in cargos or not cargos[ano]:
            cargos[ano] = {}
        if mes not in cargos[ano] or not cargos[ano][mes]:
            cargos[ano][mes] = []
        
        archivo = '{}{}'.format(d,a)
        with open(archivo, 'r', encoding='iso-8859-1') as f:
            try:
                for linea in f:
                    campos = []
                    if ';' in linea:
                        campos = linea.split(';')
                        dni = campos[5].split(' ')[-1]

                    elif '\t' in linea:
                        campos = linea.split('\t')
                        dni = campos[6].strip()
                    else:
                        continue
                    dependencia = campos[1]
                    nombre = campos[0].strip()
                    cargo = campos[3].strip()

                    try:
                        if int(dependencia.strip()) == 9 and (cargo[-3] in ['A','B','C','D','E'] or cargo in ['30E','29E']):
                        #if int(dependencia.strip()) == 9:
                            #print(f'{archivo} {nombre} {dni} {cargo}')
                            cargos[ano][mes].append({
                                'nombre': nombre,
                                'dni': dni,
                                'cargo': cargo
                            })


                    except Exception as e2:
                        pass

            except Exception as e:
                logging.info(e)

    visto = {}
    cargos_procesados = {}
    for a in sorted(list(cargos.keys())):
        for m in sorted(list(cargos[a].keys())):
            for ca in cargos[a][m]:
                if ca['dni'] not in visto or visto[ca['dni']] != ca['cargo']:
                    visto[ca['dni']] = ca['cargo']
                    if a not in cargos_procesados or not cargos_procesados[a]:
                        cargos_procesados[a] = {}
                    if m not in cargos_procesados[a] or not cargos_procesados[a][m]:
                        cargos_procesados[a][m] = []
                    cargos_procesados[a][m].append(ca)

    with open('/tmp/cargos-procesados.csv','w') as f2:
        for a in sorted(list(cargos_procesados.keys())):
            for m in sorted(list(cargos_procesados[a].keys())):
                logging.info('------------------------')
                logging.info(f'------- {m}/{a} --------')
                for ca in cargos_procesados[a][m]:
                    logging.info(ca)
                    f2.write(f"{a};{m};{ca['nombre']};{ca['dni']};{ca['cargo']}\n")

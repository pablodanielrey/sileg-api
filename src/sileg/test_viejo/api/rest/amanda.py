
import requests
import os

sileg_api = 'http://127.0.0.1:5001/sileg/api/v1.0'
#usuarios_api = os.environ['USER_REST_URL']
usuarios_api = 'http://192.168.0.3:6001/users/api/v1.0'

def getEconoMail(usuario):
    if len(usuario['mails']) <= 0:
        return ''
    for m in usuario['mails']:
        if 'unlp.edu.ar' in m['email']:
            return m['email']
    return ''

if __name__ == '__main__':

    cargosA = requests.get('http://127.0.0.1:5001/sileg/api/v1.0/cargos/').json()
    cargos = {}
    for c in cargosA:
        cargos[c['id']] = c

    """
    deptos = requests.get('http://127.0.0.1:5001/sileg/api/v1.0/departamentos').json()
    for d in deptos:
        did = d['id']
        materias = requests.get('http://127.0.0.1:5001/sileg/api/v1.0/materias/?d={}'.format(did)).json()
        for m in materias:
            print('''
Departamento: {}
Materia: {}
Cátedra: {}
            '''.format(d['nombre'], m['materia']['nombre'], m['nombre']))
    """

    with open('/tmp/sileg.csv','w') as f:

        desig = requests.get(sileg_api + '/designaciones').json()
        for d in desig:

            m = {'nombre':'-'}
            cid = d['lugar_id']
            cs = requests.get(sileg_api + '/catedras/' + cid).json()
            if len(cs) <= 0:
                ''' no es una catedra '''
                continue

            c = cs[0]
            cargo = cargos[d['cargo_id']]
            uid = d['usuario_id']
            u = requests.get(usuarios_api + '/usuarios/' + uid).json()[0]

            datos = {
                'departamento': c['padre']['nombre'],
                'materia': c['materia']['nombre'],
                'catedra': c['nombre'],
                'persona': u['dni'] + ' ' + u['nombre'] + ' ' + u['apellido'],
                'email': getEconoMail(u),
                'cargo': cargo['nombre'] + ' ' + cargo['tipo']
            }


            f.write(datos['departamento'] + ',' + datos['materia'] + ',' + datos['catedra'] + ',' + datos['persona'] + ',' + datos['email'] + ',' + datos['cargo'] + '\n')

            print('''
    Departamento: {}
    Materia: {}
    Catedra: {}
    Persona: {}
    Email: {}
    Cargo: {}
            '''.format(
                datos['departamento'],
                datos['materia'],
                datos['catedra'],
                datos['persona'],
                datos['email'],
                datos['cargo']
            ))

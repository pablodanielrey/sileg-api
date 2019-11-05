
import requests
from requests.auth import HTTPBasicAuth
import os


usuarios_api = os.environ['USER_REST_URL']
sileg_api = os.environ['SILEG_REST_URL']
usuario_mautic = os.environ['MAUTIC_PROD_USER']
clave_mautic = os.environ['MAUTIC_PROD_PASSWORD']
mautic_api = os.environ['MAUTIC_PROD_REST_URL']


def getEconoMail(usuario):
    if len(usuario['mails']) <= 0:
        return None
    for m in usuario['mails']:
        if 'unlp.edu.ar' in m['email']:
            return m['email']
    return None

def obtenerSegmentos():
    segmentos = requests.get(mautic_api + 'segments/?start=0&limit=100', auth=HTTPBasicAuth(usuario_mautic, clave_mautic)).json()
    total = segmentos["total"]
    limit = int(total / 100)
    retorno = list(segmentos["lists"].values())
    for i in range(0, limit):
        start = (i + 1) * 100
        url = "{}segments/?start={}&limit=100".format(mautic_api, start)
        r = requests.get(url, auth=HTTPBasicAuth(usuario_mautic, clave_mautic)).json()
        retorno.extend(list(r["lists"].values()))

    return retorno

def obtenerMiembrosSegmento(alias_segmento):
    users = requests.get(mautic_api + 'contacts/?search=segment:' + alias_segmento, auth=HTTPBasicAuth(usuario_mautic, clave_mautic)).json()
    return users["contacts"].values() if len(users["contacts"]) > 0 else []

def agregarMiembro(uid, sid):
    url = "{}segments/{}/contact/add/{}".format(mautic_api, sid, uid)
    print(url)
    return requests.post(url, auth=HTTPBasicAuth(usuario_mautic, clave_mautic)).json()

def parseUser(u):
    fields = u["fields"]
    core = fields["core"]
    email = core["email"]["value"]
    name = core["firstname"]["value"]
    lastname = core["lastname"]["value"]

    return {"name":name, "lastname":lastname, "email":email}

'''
segmento:
{
    name: Segment name is the only required field,
    alias: Name alias generated automatically if not set,
    description: A description of the segment,
    isPublished: A value of 0 or 1,
    isGlobal: boolean
}
'''
def crearSegmento(segmento):
    return requests.post(mautic_api + 'segments/new', auth=HTTPBasicAuth(usuario_mautic, clave_mautic), data=segmento).json()

# usuario = {'nombre':"", "apellido":"", "email": ""}
def crearUsuario(usuario):
    data = {'firstname':usuario["nombre"], 'lastname':usuario["apellido"], "email":usuario["email"]}
    return requests.post(mautic_api + 'contacts/new', auth=HTTPBasicAuth(usuario_mautic, clave_mautic), data=data).json()

def normalizarAlias(alias):
    return alias.lower().replace(".","-").replace(" ","").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(":","").replace(",","").replace("(","").replace(")","")

# user: {'nombre':"", "apellido":"", "email": ""}
# members: arreglo de usuarios de mautic
def esMiembro(user, members):
    for m in members:
        u = parseUser(m)
        if user["email"] == u["email"]:
            return True
    return False

def obtenerUsuario(u):
    users = requests.get(mautic_api + 'contacts/?search=email:' + u["email"], auth=HTTPBasicAuth(usuario_mautic, clave_mautic)).json()
    return users["contacts"]

if __name__ == '__main__':

    # obtengo los segmentos
    segmentos = {}
    for s in obtenerSegmentos():
        segmentos[s["alias"]] = {"id":s["id"],"name":s["name"], "alias":s["alias"]}

    # obtengo los cargos
    cargosA = requests.get(sileg_api + '/cargos').json()
    cargos = {}
    for c in cargosA:
        cargos[c['id']] = c


    result = {}
    desig = requests.get(sileg_api + '/designaciones').json()
    i = 0
    for d in desig:
        i = i + 1
        print("procesando desginacion {} de {}".format(i, len(desig)))
        m = {'nombre':'-'}
        cid = d['lugar_id']
        cs = requests.get(sileg_api + '/catedras/' + cid).json()
        if len(cs) <= 0:
            ''' no es una catedra '''
            continue

        c = cs[0]
        cargo = cargos[d['cargo_id']]
        uid = d['usuario_id']
        u = requests.get(usuarios_api + '/usuarios/' + uid).json()
        email = getEconoMail(u)
        if email is None:
            continue

        departamento = c['padre']['nombre']
        materia = c['materia']['nombre']

        # nombre = '{}.{}.{}'.format(departamento, materia, cargo['nombre'])
        # id = c['padre']['id'] + c['materia']['id'] + d['cargo_id']
        nombre = '{}.{}'.format(departamento, cargo['nombre'])
        id = c['padre']['id'] + d['cargo_id']

        user = {'nombre':u["nombre"], "apellido":u["apellido"], "email": email}
        if id in result:
            r = result[id]
            r["usuarios"].append(user)
        else:
            result[id] = {'nombre': nombre, 'usuarios':[user]}


    for value in result.values():
        seg = {"name":value["nombre"], "alias":normalizarAlias(value["nombre"])}

        segmento = {}
        print(seg["alias"])
        if seg["alias"] in segmentos:
            print("ya existe el segmento: " + seg["alias"])
            segmento = segmentos[seg["alias"]]
        else:
            print("creando segmento " + seg["alias"])
            segmento = crearSegmento(seg)["list"]

        # debo agregar los miembros al segmento
        miembros = obtenerMiembrosSegmento(seg['alias'])
        for u in value["usuarios"]:
            if esMiembro(u, miembros):
                continue
            print("agregando miembro {}".format(u))
            usuario = obtenerUsuario(u)
            uid = None
            if len(usuario) < 1:
                print("Crear usuario: {}".format(u))
                nuevo = crearUsuario(u)
                print(nuevo)
                uid = nuevo["contact"]["id"]
            else:
                ids = list(usuario.keys())
                uid = ids[0]
            print("UID {}".format(uid))

            agregarMiembro(uid, segmento["id"])

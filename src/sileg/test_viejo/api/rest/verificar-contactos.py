from sileg.model.entities import Lugar
from sileg.model.GoogleAuthApi import GAuthApis
import requests
from requests.auth import HTTPBasicAuth
import os


mautic_prod = {"usuario": os.environ['MAUTIC_PROD_USER'], "clave": os.environ['MAUTIC_PROD_PASSWORD'], "url": os.environ['MAUTIC_PROD_REST_URL']}
mautic_old = {"usuario": os.environ['MAUTIC_OLD_USER'], "clave": os.environ['MAUTIC_OLD_PASSWORD'], "url": os.environ['MAUTIC_OLD_REST_URL']}

def normalizarNombre(nombre):
    return nombre.lower().replace(".","-").replace(" ","-").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n").replace(":","").replace(",","").replace("(","").replace(")","")

def esCorreo(email):
    r = email.strip().split('@')
    return len(r) > 1 and r[1] != ''

def obtenerUsuario(email, mautic):
    r = requests.get(mautic["url"] + 'contacts/?search=email:' + email, auth=HTTPBasicAuth(mautic["usuario"], mautic["clave"])).json()
    u = list(r["contacts"].values())[0] if int(r["total"]) > 0 else None
    return u

def obtenerSegmento(titulo, mautic):
    print("Buscando segmento " + titulo)
    r = requests.get(mautic["url"] + 'segments/?search=name:' + titulo, auth=HTTPBasicAuth(mautic["usuario"], mautic["clave"])).json()
    return list(r["lists"].values())[0] if int(r["total"]) > 0 else None

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
def crearSegmento(segmento, mautic):
    s = requests.post(mautic["url"] + 'segments/new', auth=HTTPBasicAuth(mautic["usuario"], mautic["clave"]), data=segmento).json()
    return s["list"]


# usuario = {'nombre':"", "apellido":"", "email": ""}
def crearUsuario(usuario, mautic):
    data = {'firstname':usuario["nombre"], 'lastname':usuario["apellido"], "email":usuario["email"]}
    u = requests.post(mautic["url"] + 'contacts/new', auth=HTTPBasicAuth(mautic["usuario"], mautic["clave"]), data=data).json()
    return u["contact"] if "contact" in u else None

def agregarMiembro(uid, sid, mautic):
    url = "{}segments/{}/contact/add/{}".format(mautic["url"], sid, uid)
    return requests.post(url, auth=HTTPBasicAuth(mautic["usuario"], mautic["clave"])).json()


def obtenerMiembrosSegmento(alias_segmento, mautic):
    users = requests.get(mautic["url"] + 'contacts/?search=segment:' + alias_segmento, auth=HTTPBasicAuth(mautic["usuario"], mautic["clave"])).json()
    return users["contacts"].values() if len(users["contacts"]) > 0 else []

def obtenerCorreos(service, spreadsheetId, sheet):
    range = sheet + "!A2:A"
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range).execute()
    values = result.get('values', [])
    emails = set()
    if values:
        for row in values:
            if len(row) > 0 and esCorreo(row[0]):
                emails.add(row[0].strip())

    print("La hoja {} tiene {} emails".format(sheet, len(emails)))
    return emails

if __name__ == '__main__':


    service = GAuthApis.getServiceSheet()

    spreadsheetId = os.environ['SPREADSHEET_ID']
    ranges = []
    include_grid_data = False

    result = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheets = result["sheets"]

    contactos = []
    for s in sheets:
        prop = s["properties"]
        sheet = prop["title"]
        emails = obtenerCorreos(service, spreadsheetId, sheet)
        contactos.append({"titulo": sheet, "correos": emails})

    correosIncorrectos = set()
    for a in contactos:
        titulo = normalizarNombre(a["titulo"])
        segmento = obtenerSegmento(titulo, mautic_old)
        if segmento is None:
            print("crear segmento " + titulo)
            s = {"name": titulo, "alias": titulo}
            segmento = crearSegmento(s, mautic_old)
        miembros = list(obtenerMiembrosSegmento(segmento["alias"], mautic_old))
        ids = [m["id"] for m in miembros]
        # recorro todos los correos
        for correo in a["correos"]:
            u = obtenerUsuario(correo, mautic_prod)
            print("procesando {}".format(correo))
            if u is None:
                u = obtenerUsuario(correo, mautic_old)
                if u is None:
                    u = {"nombre":"", "apellido": "", "email":correo}
                    print("crear usuario")
                    u = crearUsuario(u, mautic_old)
                    if u is None:
                        correosIncorrectos.add(correo)
                        print("error: correo {} formato invalido".format(correo))
                        continue

                print("ID: {}".format(u["id"]))
                if u["id"] in ids:
                    print("Ya existe en el segmento")
                else:
                    print("agregando contacto al segmento " + titulo)
                    agregarMiembro(u["id"], segmento["id"], mautic_old)
                    
    print("Correos incorrecto {}".format(correosIncorrectos))

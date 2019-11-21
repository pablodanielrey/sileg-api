
import requests

def getStates():
    r = requests.get('https://apis.datos.gob.ar/georef/api/provincias')
    if r.ok:
        js = r.json()
        ps = [(j['id'], j['nombre']) for j in js['provincias']]
        ps.insert(0,('0','Seleccione una Provincia'))
        return ps
    else:
        return {('0','Sin opciones')}
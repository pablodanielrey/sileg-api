
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

def searchCity(search=None):
    if search:
        r = requests.get(f'https://apis.datos.gob.ar/georef/api/localidades?nombre={search}&campos=nombre,provincia.nombre')
        if r.ok:
            js = r.json()
            print(js)
            options = [{'nombre': f'{j["nombre"]} {j["provincia"]["nombre"]}'} for j in js['localidades']]
            return options
        else:
            return [{'error':'API Error'}]
    else:
        return [{'error':'Debe proporcionarse datos de busqueda'}]
import json
from sileg.helpers.apiHandler import searchCity
from flask import request, url_for

from . import bp

@bp.route('/buscar')
def search():
    """
    Api de busqueda de ciudades
    """
    search = request.args.get('query',None)
    result = searchCity(search)
    return json.dumps(result)
    
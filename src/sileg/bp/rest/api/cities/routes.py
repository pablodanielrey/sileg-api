import json
from sileg.helpers.apiHandler import searchCity
from flask import request, url_for

from . import bp

@bp.route('/buscar')
def search():
    """
    Api de busqueda de ciudades
    """
    result = searchCity('bera')
    return json.dumps(result)
    
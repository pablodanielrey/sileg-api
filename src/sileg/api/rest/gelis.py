
from flask import Blueprint, request
from .converters import ListConverter

bp = Blueprint('gelis', __name__, url_prefix='/gelis/api/v1.0')

@bp.before_app_request
def antes_de_cada_requerimiento():
    pass

@bp.route('/designaciones', methods=['GET'])
def designaciones_por_lugares():
    lids = request.args.get('lids',None)
    if not lids:
        return (400,'Invalid')

    return []
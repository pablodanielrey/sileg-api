from flask import Blueprint

bp = Blueprint('cities', __name__)

from sileg.bp.rest.api.cities import routes
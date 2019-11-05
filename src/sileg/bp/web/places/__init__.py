from flask import Blueprint

bp = Blueprint('places', __name__, template_folder='templates')

from sileg.bp.web.places import routes
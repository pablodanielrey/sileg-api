from flask import Blueprint

bp = Blueprint('logs', __name__, template_folder='templates')

from sileg.bp.web.logs import routes

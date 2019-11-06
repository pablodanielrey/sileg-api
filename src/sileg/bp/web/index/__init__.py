from flask import Blueprint

bp = Blueprint('index', __name__, template_folder='templates')

from sileg.bp.web.index import routes
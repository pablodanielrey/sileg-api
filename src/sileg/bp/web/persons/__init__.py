from flask import Blueprint

bp = Blueprint('persons', __name__, template_folder='templates')

from sileg.bp.web.persons import routes
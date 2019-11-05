from flask import Blueprint

bp = Blueprint('designations', __name__, template_folder='templates')

from sileg.bp.web.designations import routes
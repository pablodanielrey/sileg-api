from flask import Blueprint

bp = Blueprint('students', __name__, template_folder='templates')

from sileg.bp.web.students import routes
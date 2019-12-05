from flask import Blueprint

bp = Blueprint('leavelicense', __name__, template_folder='templates')

from sileg.bp.web.leavelicense import routes
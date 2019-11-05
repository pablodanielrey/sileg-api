from flask import Blueprint

bp = Blueprint('places', __name__, template_folder='templates')

from src.sileg.bp.web.designations import routes
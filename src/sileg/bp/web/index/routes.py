from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp

from sileg.auth import require_user

@bp.route('/')
@require_user
def index(user):
    """
    Pagina principal del sistema
    """
    return render_template('index.html', user=user)
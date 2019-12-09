from flask import render_template, flash, redirect,request, Markup, url_for

from sileg.auth import oidc
from . import bp


@bp.route('/login')
@oidc.require_login
def login():
    return oidc.user_getfield('email')

@bp.route('/')
def index():
    """
    Pagina principal del sistema
    """
    if oidc.user_loggedin:
        user = oidc.user_getinfo(['firstname', 'lastname', 'email', 'sub'])
        return render_template('index.html', user=user)
    else:
        return "no logueado"


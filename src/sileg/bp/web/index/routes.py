from flask import render_template, flash, redirect,request, Markup, url_for

from sileg.auth import oidc, render_templateOICDV1
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
        user = oidc.user_getinfo(['given_name', 'family_name', 'preferred_username', 'email_verified', 'email', 'sub'])
        return render_template('index.html', user=user)
    else:
        return "no logueado"

@bp.route('/v1')
def indexv1():
    """
    Pagina principal del sistema
    """
    if oidc.user_loggedin:
        return render_templateOICDV1('index.html','Esta variable','estootro')
    else:
        return "no logueado"

def render_templateOICDV2(fn):
    @bp.context_processor
    def additional_context():
        if request.endpoint.split('.')[1] != fn.__name__:
            return {} 
        user = oidc.user_getinfo(['given_name', 'family_name', 'preferred_username', 'email_verified', 'email', 'sub'])
        return {
            'user': user,
        }
    return fn

@bp.route('/v2')
@render_templateOICDV2
def indexv2():
    """
    Pagina principal del sistema
    """
    if oidc.user_loggedin:
        data = 'algo'
        return render_template('index.html', data=data)
    else:
        return "no logueado"
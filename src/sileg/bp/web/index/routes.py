from flask import render_template, flash, redirect,request, Markup, url_for

from sileg.auth import require_user
from . import bp


@bp.route('/login')
@require_user
def login(user):
    return user['email']

@bp.route('/')
@require_user
def index(user):
    """
    Pagina principal del sistema
    """
    if user:
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

def render_templateOICDV2(*args, **kwargs):
    bp = kwars['blueprint']
    @bp.context_processor
    def additional_context(fn):
        #if request.endpoint.split('.')[1] != fn.__name__:
        #    return {} 
        user = oidc.user_getinfo(['given_name', 'family_name', 'preferred_username', 'email_verified', 'email', 'sub'])
        return {
            'user': user,
        }
    return fn



@bp.route('/v2')
@require_user
def indexv2(user):
    """
    Pagina principal del sistema
    """
    if user:
        data = 'algo'
        return render_template('index.html', data=data, user=user)
    else:
        return "no logueado"
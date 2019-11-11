from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import UserCreateForm

from . import bp

@bp.route('/crear')
def create():
    """
    Pagina principal de usuarios
    """
    form = UserCreateForm()
    return render_template('create.html',form=form)

@bp.route('/buscar')
def search():
    """
    Pagina principal de usuarios
    """
    return render_template('users.html')
    

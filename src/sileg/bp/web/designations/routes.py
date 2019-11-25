from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import DesignationCreateForm

from . import bp

@bp.route('/crear')
def create():
    """
    Pagina de creacion de designacion
    """
    form = DesignationCreateForm()
    user = {
        'dni': '12345678',
        'firstname': 'Pablo',
        'lastname': 'Rey'
    }
    return render_template('createDesignations.html', user=user, form=form)

@bp.route('/buscar')
def search():
    """
    Pagina de busqueda de desiganacion
    """
    return render_template('searchDesignations.html')
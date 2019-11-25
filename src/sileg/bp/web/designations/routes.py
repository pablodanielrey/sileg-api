from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import ExtendDesignationForm

from . import bp

@bp.route('/crear')
def create():
    """
    Pagina de creacion de designacion
    """
    return render_template('createDesignations.html')

@bp.route('/buscar')
def search():
    """
    Pagina de busqueda de desiganacion
    """
    return render_template('searchDesignations.html')

@bp.route('/extension/crear')
def extend():
    """
    Pagina de creacion de extension
    """
    form = ExtendDesignationForm()
    return render_template('createExtension.html',form=form)
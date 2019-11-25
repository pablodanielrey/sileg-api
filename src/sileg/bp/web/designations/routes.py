from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import ExtendDesignationForm, RenewForm, DesignationCreateForm

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

@bp.route('/extension/crear')
def extend():
    """
    Pagina de creacion de extension
    """
    form = ExtendDesignationForm()
    return render_template('createExtension.html',form=form)

@bp.route('/prorroga/crear')
def renew():
    """
    Pagina de creacion de prorroga
    """
    form = RenewForm()
    return render_template('createRenew.html',form=form)
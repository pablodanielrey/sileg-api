from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import ExtendDesignationForm, RenewForm, DesignationCreateForm, DesignationSearchForm

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
    Pagina de busqueda de desiganaciones
    """
    designations = [{
            'firstname':'Pablo',
            'lastname':'Rey',
            'subject':'Ingles I',
            'chair':'Original',
            'workArea': '-',
            'workPlace': '-',
            'observations': '-',
            'positionType': 'A/D',
            'character': 'INT',
        },{
            'firstname':'Emanuel',
            'lastname':'Pais',
            'subject':'Contabilidad III',
            'chair':'Original',
            'workArea': '-',
            'workPlace': '-',
            'observations': '-',
            'positionType': 'ADJ',
            'character': 'SUP',
        },
        {
            'firstname':'Miguel',
            'lastname':'Macagno',
            'subject':'Administración I',
            'chair':'B',
            'workArea': '-',
            'workPlace': '-',
            'observations': '-',
            'positionType': 'JAD',
            'character': 'INT',
        },
        {
            'firstname':'Leonardo',
            'lastname':'Consolini',
            'subject':'Administración I',
            'chair':'A',
            'workArea': '-',
            'workPlace': '-',
            'observations': '-',
            'positionType': 'TIT',
            'character': 'INT',
        }
    ]
    form = DesignationSearchForm()
    return render_template('searchDesignations.html',designations=designations,form=form)

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
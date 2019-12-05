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
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'A/D',
            'character': 'INT',
        },{
            'firstname':'Emanuel',
            'lastname':'Pais',
            'subject':'Contabilidad III',
            'chair':'Original',
            'dedication': 'Semi-dedicación',
            'observations': '-',
            'positionType': 'ADJ',
            'character': 'SUP',
        },
        {
            'firstname':'Miguel Angel Jesús',
            'lastname':'Macagno',
            'subject':'Administración I',
            'chair':'B',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'JAD',
            'character': 'INT',
        },
        {
            'firstname':'Leonardo',
            'lastname':'Consolini',
            'subject':'Administración I',
            'chair':'A',
            'dedication': 'Exclusiva',
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

@bp.route('/listado')
def personDesignations():
    """
    Pagina de lisata de designaciones de una persona
    Recibe como parametro uid de la persona
    """
    person = {
        'firstname':'Pablo',
        'lastname':'Rey',
        'person_number': '12345678',
        'birthdate': '02/12/1979',
        'address': 'Calle 6 Nº 667, La Plata, Buenos Aires.'
    }
    designations = [{
            'subject':'Ingles I',
            'chair':'Original',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'A/D',
            'character': 'INT',
        },{
            'subject':'Contabilidad III',
            'chair':'Original',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'ADJ',
            'character': 'SUP',
        },
        {
            'subject':'Administración I',
            'chair':'B',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'JAD',
            'character': 'INT',
        },
        {
            'subject':'Administración I',
            'chair':'A',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'TIT',
            'character': 'INT',
        }
    ]
    return render_template('listPersonDesignations.html',designations=designations,person=person)

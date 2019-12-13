from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp

from .forms import ExtendDesignationForm, RenewForm, DesignationCreateForm, DesignationSearchForm

from sileg.auth import require_user

@bp.route('/crear')
@require_user
def create(user):
    """
    Pagina de creacion de designacion
    """
    form = DesignationCreateForm()
    person = {
        'dni': '12345678',
        'firstname': 'Pablo',
        'lastname': 'Rey'
    }
    return render_template('createDesignations.html', user=user, person=person,form=form)

@bp.route('/buscar')
@require_user
def search(user):
    """
    Pagina de busqueda de desiganaciones
    """
    designations = [{
            'firstname':'Pablo',
            'lastname':'Rey',
            'place':'Ingles I',
            'placetype':'Original',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'A/D',
            'character': 'INT',
            'relatedTo': None
        },
        {
            'firstname':'Pablo',
            'lastname':'Rey',
            'place':'Seminario de Ingles',
            'placetype':'Original',
            'dedication': 'Exclusiva',
            'positionType': 'Cumpliendo funcion',
            'character': 'INT',
            'relatedTo': True
        },
        {
            'firstname':'Emanuel',
            'lastname':'Pais',
            'place':'Contabilidad III',
            'placetype':'Original',
            'dedication': 'Semi-dedicación',
            'observations': '-',
            'positionType': 'ADJ',
            'character': 'SUP',
            'relatedTo': None
        },
        {
            'firstname':'Miguel Angel Jesús',
            'lastname':'Macagno',
            'place':'Administración I',
            'placetype':'B',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'JAD',
            'character': 'INT',
            'relatedTo': None
        },
        {
            'firstname':'Leonardo',
            'lastname':'Consolini',
            'place':'Administración I',
            'placetype':'A',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'TIT',
            'character': 'INT',
            'relatedTo': None
        }
    ]
    form = DesignationSearchForm()
    return render_template('searchDesignations.html',user=user,designations=designations,form=form)

@bp.route('/extension/crear')
@require_user
def extend():
    """
    Pagina de creacion de extension
    """
    form = ExtendDesignationForm()
    return render_template('createExtension.html',user=user,form=form)

@bp.route('/prorroga/crear')
@require_user
def renew():
    """
    Pagina de creacion de prorroga
    """
    form = RenewForm()
    return render_template('createRenew.html',user=user,form=form)

@bp.route('/listado')
@require_user
def personDesignations(user):
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
            'place':'Ingles I',
            'placetype':'Original',
            'dedication': 'Exclusiva',
            'positionType': 'A/D',
            'character': 'INT',
            'relatedTo': None
        },
        {
            'place':'Seminario de Ingles',
            'placetype':'Original',
            'dedication': 'Exclusiva',
            'positionType': 'Cumpliendo funcion',
            'character': 'INT',
            'relatedTo': True
        },
        {
            'place':'Contabilidad III',
            'placetype':'Original',
            'dedication': 'Exclusiva',
            'positionType': 'ADJ',
            'character': 'SUP',
            'relatedTo': None
        },
        {
            'place':'Administración I',
            'placetype':'B',
            'dedication': 'Exclusiva',
            'positionType': 'JAD',
            'character': 'INT',
            'relatedTo': None
        },
        {
            'place':'Administración I',
            'placetype':'A',
            'dedication': 'Exclusiva',
            'positionType': 'TIT',
            'character': 'INT',
            'relatedTo': None
        }
    ]
    return render_template('listPersonDesignations.html',user=user,designations=designations,person=person)

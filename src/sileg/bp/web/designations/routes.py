from flask import render_template, flash, redirect,request, Markup, url_for, abort

from sileg.auth import require_user
from sileg.models import silegModel, open_sileg_session, usersModel, open_users_session

from . import bp
from .forms import ExtendDesignationForm, RenewForm, DesignationCreateForm, DesignationSearchForm


@bp.route('/crear/{uid}', methods=['GET'])
@require_user
def create_get(user, uid):
    """
        Pagina de creacion de designacion
    """
    assert uid is not None

    with open_users_session() as session:
        person = usersModel.get_users(session, uids=[uid])[0]

    form = DesignationCreateForm()
    with open_sileg_session() as session:
        form._load_values(session, silegModel)
 
    return render_template('createDesignations.html', user=user, person=person, form=form)

@bp.route('/crear/{uid}', methods=['POST'])
@require_user
def create_post(user, uid):
    """
        Pagina de creacion de designacion
    """
    assert uid is not None

    with open_users_session() as session:
        person = usersModel.get_users(session, uids=[uid])[0]

    form = DesignationCreateForm()
    if form.validate_on_submit():
        return 
    else:
        abort(404)

    return render_template('createDesignations.html', user=user, person=person, form=form)


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
def extend(user):
    """
    Pagina de creacion de extension
    """
    form = ExtendDesignationForm()
    return render_template('createExtension.html', user=user, form=form)

@bp.route('/prorroga/crear')
@require_user
def renew(user):
    """
    Pagina de creacion de prorroga
    """
    form = RenewForm()
    return render_template('createRenew.html', user=user, form=form)

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
    return render_template('listPersonDesignations.html', user=user, designations=designations, person=person)

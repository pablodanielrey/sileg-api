from flask import render_template, flash, redirect,request, Markup, url_for, abort
from . import bp

from .forms import PersonCreateForm, PersonSearchForm, TitleAssignForm, PersonModifyForm

from sileg.auth import require_user

from sileg.auth import oidc
from sileg.models import usersModel, open_users_session

@bp.route('/crear',methods=['GET','POST'])
@require_user
def create(user):
    """
    Pagina principal de personas
    """
    form = PersonCreateForm()
    if form.validate_on_submit():
        form.save(user['sub'])
    return render_template('createPerson.html', user=user, form=form)

@bp.route('/buscar')
@require_user
def search(user):
    """
    Pagina principal de personas
    """
    form = PersonSearchForm()
    query = request.args.get('query','',str)
    persons = []
    if query:
        with open_users_session() as session:
            uids = usersModel.search_user(session, query)
            persons = usersModel.get_users(session, uids)
    return render_template('searchPerson.html', user=user, persons=persons, form=form)

@bp.route('<uid>/titulos')
@require_user
def degrees(user,uid):
    """
    Pagina de Listado de Títulos de persona
    """
    person = {
        'dni': '12345678',
        'firstname': 'Pablo',
        'lastname': 'Rey'
    }
    titles = [{
        'titleType' : 'Grado',
        'titleDate' : '1998-12-15',
        'titleName' : 'Secundario',
        'titleFile' : 'fileId.pdf'
    },
    {
        'titleType' : 'Grado',
        'titleDate' : '2020-12-15',
        'titleName' : 'Licenciado en Sistemas',
        'titleFile' : 'fileId.pdf'
    },
    {
        'titleType' : 'Posgrado',
        'titleDate' : '2025-12-15',
        'titleName' : 'Doctorado en Ciencias Informáticas',
        'titleFile' : 'fileId.pdf'
    }]
    form = TitleAssignForm()
    return render_template('showDegrees.html', user=user,person=person, titles=titles, form=form)

@bp.route('<uid>')
@require_user
def personData(user,uid):
    """
    Pagina de vista de datos personales
    """
    with open_users_session() as session:
        persons = usersModel.get_users(session, [uid])
        if not persons or len(persons) <= 0:
            abort(404)
        person = persons[0]

    return render_template('showPerson.html', user=user,person=person)

@bp.route('<uid>/modificar')
@require_user
def modifyPersonData(user,uid):
    """
    Pagina de vista de datos personales
    """
    with open_users_session() as session:
        persons = usersModel.get_users(session, [uid])
        if not persons or len(persons) <= 0:
            abort(404)
        person = persons[0]
        form = PersonModifyForm()
        if form.validate_on_submit():
            form.save(user['sub'])

    return render_template('modifyPerson.html', user=user, person=person, form=form)
    

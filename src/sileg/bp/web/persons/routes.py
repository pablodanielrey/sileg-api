from flask import render_template, flash, redirect,request, Markup, url_for, abort
from . import bp

from .forms import PersonCreateForm, PersonSearchForm, TitleAssignForm

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

@bp.route('<uid>/titulos',methods=['GET','POST'])
@require_user
def degrees(user,uid):
    """
    Pagina de Listado de Títulos de persona
    """
    form = TitleAssignForm()
    with open_users_session() as session:
        persons = usersModel.get_users(session, [uid])
        if not persons or len(persons) <= 0:
            abort(404)
        person = persons[0]
        titles = usersModel.get_person_titles(session,uid)
    if form.validate_on_submit():
        form.save(uid,user['sub'])
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
    

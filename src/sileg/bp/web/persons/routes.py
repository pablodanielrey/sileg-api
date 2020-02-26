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
        if person.lastname:
            form.lastname.data = person.lastname
        if person.firstname:
            form.firstname.data = person.firstname
        if len(person.identity_numbers) > 0:
            for pi in person.identity_numbers:
                if pi.type.value != 'CUIL' and pi.type.value != 'CUIT':
                    form.person_number_type.data = pi.type.value
                    form.person_number.data = pi.number
                else:
                    form.laboral_number.data = pi.number
        if person.gender:
            form.gender.data = person.gender
        if person.marital_status:
            form.marital_status.data = person.marital_status
        if person.birthplace:
            form.birthplace.data = person.birthplace
        if person.birthdate:
            form.birthdate.data = person.birthdate.strftime('%d/%m/%Y')
        if person.address:
            form.address.data = person.address
        if person.residence:
            form.residence.data = person.residence
        if len(person.mails) > 0:
            for pm in person.mails: 
                if pm.type.value == 'INSTITUTIONAL':
                    form.work_email.data = pm.email
                if pm.type.value == 'ALTERNATIVE':
                    form.personal_email.data = pm.email
        if len(person.phones) > 0:
            for ph in person.phones:
                if ph.type.value == 'LANDLINE':
                    form.land_line.data = ph.number
                if ph.type.value == 'CELLPHONE':
                    form.mobile_number == ph.number
        if form.validate_on_submit():
            form.save(user['sub'])

    return render_template('modifyPerson.html', user=user, form=form)
    

from flask import render_template, flash, redirect,request, Markup, url_for
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
        data = {
            'lastname' : form.lastname.data,
            'firstname' : form.firstname.data,
            'person_number_type' : form.person_number_type.data,
            'person_number' : form.person_number.data,
            'gender' : form.gender.data,
            'marital_status' : form.marital_status.data,
            'birthplace' : form.birthplace.data,
            'birthdate' : form.birthdate.data,
            'residence' : form.residence.data,
            'address' : form.address.data,
            'work_email' : form.work_email.data,
            'personal_email' : form.personal_email.data,
            'land_line' : form.land_line.data,
            'mobile_number' : form.mobile_number.data,
            'person_numberFile' : form.person_numberFile.data,
            'laboral_numberFile' : form.laboral_numberFile.data,
            'seniority_external_years' : form.seniority_external_years.data,
            'seniority_external_months'  : form.seniority_external_months.data,
            'seniority_external_days' : form.seniority_external_days.data,
        }
        print(data)
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
        person = usersModel.get_users(session, [uid])[0]
    return render_template('showPerson.html', user=user,person=person)
    

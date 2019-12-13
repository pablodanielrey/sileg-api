from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import PersonCreateForm, PersonSearchForm, TitleAssignForm

import users.model

from sileg.auth import oidc
from sileg.models import usersModel


from . import bp

@bp.route('/crear',methods=['GET','POST'])
def create():
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

    user = oidc.user_getinfo(['given_name', 'family_name', 'preferred_username', 'email_verified', 'email', 'sub']) 
    
    return render_template('createPerson.html', form=form, user=user)

@bp.route('/buscar')
def search():
    """
    Pagina principal de personas
    """
    persons = [{
        'firstname':'Pablo',
        'lastname':'Rey',
        'person_number': '12345678'
    },
    {
        'firstname':'Emanuel',
        'lastname':'Pais',
        'person_number': '12345678'
    },
    {
        'firstname':'Miguel Angel Jesús',
        'lastname':'Macagno',
        'person_number': '12345678'
    },
    {
        'firstname':'Leonardo',
        'lastname':'Consolini',
        'person_number': '12345678'
    }]

    user = oidc.user_getinfo(['given_name', 'family_name', 'preferred_username', 'email_verified', 'email', 'sub'])

    form = PersonSearchForm()
    query = request.args.get('query','',str)

    persons = []
    if query:
        with users.model.open_session() as session:
            uids = usersModel.search_user(session, query)
            persons = usersModel.get_users(session, uids)

    return render_template('searchPerson.html', persons=persons, form=form, user=user)

@bp.route('<uid>/titulos')
def degrees(uid):
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

    user = oidc.user_getinfo(['given_name', 'family_name', 'preferred_username', 'email_verified', 'email', 'sub'])

    return render_template('showDegrees.html', person=person, titles=titles, form=form, user=user)
    

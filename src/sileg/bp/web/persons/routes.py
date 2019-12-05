from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import PersonCreateForm, PersonSearchForm

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
    print(form.errors)  
    return render_template('createPerson.html',form=form)

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
    form = PersonSearchForm()
    query = request.args.get('query','',str)
    return render_template('searchPerson.html', persons=persons, form=form)
    

from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import PersonCreateForm, PersonSearchForm

from . import bp

@bp.route('/crear')
def create():
    """
    Pagina principal de personas
    """
    form = PersonCreateForm()
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
    

from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import UserCreateForm, UserSearchForm

from . import bp

@bp.route('/crear')
def create():
    """
    Pagina principal de usuarios
    """
    form = UserCreateForm()
    return render_template('createUser.html',form=form)

@bp.route('/buscar')
def search():
    """
    Pagina principal de usuarios
    """
    users = [{
        'firstname':'Pablo',
        'lastname':'Rey',
    },
    {
        'firstname':'Emanuel',
        'lastname':'Pais',
    },
    {
        'firstname':'Miguel',
        'lastname':'Macagno',
    },
    {
        'firstname':'Leonardo',
        'lastname':'Consolini'
    }]
    form = UserSearchForm()
    query = request.args.get('query','',str)
    return render_template('searchUsers.html', users=users, form=form)
    

from flask import render_template, flash, redirect,request, Markup, url_for
from sileg.auth import require_user

from .forms import PlaceSearchForm

from . import bp

@bp.route('/crear')
@require_user
def create(user):
    """
    Pagina de creacion de usuarios GET
    """
    return render_template('places.html',user=user)

@bp.route('/crear', methods=['POST'])
@require_user
def create_post(user):
    """
    Pagina de creacion de usuarios POST
    """
    return render_template('places.html',user=user)

@bp.route('/buscar')
@require_user
def search(user):
    """
    Pagina de busqueda de lugares
    """
    form = PlaceSearchForm()
    
    query = request.args.get('query','',str)
    places = []
    if query:
        #TODO ver metodo de busqueda de lugares
        places = None            
    else:
        places = None
    return render_template('searchPlaces.html',user=user, places=places,form=form)
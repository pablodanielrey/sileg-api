from flask import render_template, flash, redirect,request, Markup, url_for, abort
from sileg.auth import require_user

from .forms import PlaceSearchForm,PlaceCreateForm

from sileg.models import open_sileg_session, silegModel

from . import bp

@bp.route('/crear')
@require_user
def create(user):
    """
    Pagina de creacion de lugares GET
    """
    form = PlaceCreateForm()
    return render_template('createPlace.html',user=user,form=form)

@bp.route('/crear', methods=['POST'])
@require_user
def create_post(user):
    """
    Pagina de creacion de lugares POST
    """
    form = PlaceCreateForm()
    if not form.validate_on_submit():
        flash(Markup('<span>Error al crear lugar!</span>'))
        print(form.errors)
        return render_template('createPlace.html',user=user,form=form)
    if form.type.data == '0':
        flash(Markup('<span>Por favor seleccione un tipo de lugar!</span>'))
        return render_template('createPlace.html',user=user,form=form)
    with open_sileg_session() as session:     
        form.save(session, user['sub'])
        session.commit()
        flash(Markup('<span>¡Lugar Creado!</span>'))
    return redirect(url_for('places.search', query=form.name.data))

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
        #with open_sileg_session() as session:
        #    result = silegModel.
        places = None            
    else:
        places = None
    return render_template('searchPlaces.html',user=user, places=places,form=form)
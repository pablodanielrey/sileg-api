import datetime

from flask import render_template, flash, redirect,request, Markup, url_for, abort
from sileg.auth import require_user

from .forms import PlaceSearchForm,PlaceCreateForm,placeTypeToString,PlaceModifyForm

from sileg.models import open_sileg_session, silegModel

from sileg.helpers.permissionsHelper import verify_admin_permissions, verify_sileg_permission, verify_students_permission

from . import bp

@bp.route('/crear')
@require_user
@verify_admin_permissions
def create(user):
    """
    Pagina de creacion de lugares GET
    """
    with open_sileg_session() as session:
        form = PlaceCreateForm(session)
    return render_template('createPlace.html',user=user,form=form)

@bp.route('/crear', methods=['POST'])
@require_user
@verify_admin_permissions
def create_post(user):
    """
    Pagina de creacion de lugares POST
    """
    with open_sileg_session() as session:
        form = PlaceCreateForm(session)
        if not form.validate_on_submit():
            flash(Markup('<span>Error al crear lugar!</span>'))
            print(form.errors)
            return render_template('createPlace.html',user=user,form=form)
        if form.type.data == '0':
            flash(Markup('<span>Por favor seleccione un tipo de lugar!</span>'))
            return render_template('createPlace.html',user=user,form=form)     
        form.save(session, user['sub'])
        session.commit()
        flash(Markup('<span>¡Lugar Creado!</span>'))
    return redirect(url_for('places.search', query=form.name.data))

@bp.route('/organigrama')
@require_user
@verify_sileg_permission
def organigrama(user):
    """
    Organigrama de las oficinas/catedras
    """
    def _get_tree(root):
        r = {
            'root': root,
            'children': [_get_tree(c) for c in root.children]
        }
        return r

    with open_sileg_session() as session:
        result = silegModel.get_all_places(session, historic=True, deleted=True)
        if result:
            places = silegModel.get_places(session,result)
            """ genero la estructura de organigrama """
            roots = [p for p in places if p.parent_id is None]
            trees = [_get_tree(p) for p in roots]
        else:
            trees = []
    return render_template('showPlacesTree.html', user=user, places=trees, placeTypeToString=placeTypeToString)

@bp.route('/buscar')
@require_user
@verify_sileg_permission
def search(user):
    """
    Pagina de busqueda de lugares
    """
    form = PlaceSearchForm()
    
    query = request.args.get('query','',str)
    places = []
    if query:
        with open_sileg_session() as session:
            result = silegModel.search_place(session,query)
            if result:
                places = silegModel.get_places(session,result)
                places = sorted(sorted(places, key=lambda p: p.name), key=lambda p: p.type.value)
            else:
                result = []
    else:
        places = None
    return render_template('searchPlaces.html',user=user, places=places,form=form,placeTypeToString=placeTypeToString)


@bp.route('<pid>/modificar')
@require_user
@verify_admin_permissions
def modifyPlace(user,pid):
    """
    Pagina de modificacion de lugar GET
    """
    with open_sileg_session() as session:
        form = PlaceModifyForm(session, pid)
    return render_template('modifyPlace.html', user=user, form=form)

@bp.route('<pid>/modificar',methods=['POST'])
@require_user
@verify_admin_permissions
def modifyPlace_post(user,pid):
    """
    Pagina de modificacion de lugar POST
    """
    with open_sileg_session() as session:
        form = PlaceModifyForm(session)
        if form.validate_on_submit():
            ok = form.save(session,pid,user['sub'])
            if ok == pid:
                flash(Markup('<span>¡Lugar Actualizado!</span>'))
                session.commit()
                return redirect(url_for('places.search', query=form.name.data))
            else:
                flash(Markup('<span>¡Error al modificar!</span>'))
                return redirect(url_for('places.modifyPlace', pid=pid))
        if 'email' in form.errors:
            flash(Markup('<span>¡Error al actualizar correo!</span>'))
    return redirect(url_for('places.modifyPlace', pid=pid))
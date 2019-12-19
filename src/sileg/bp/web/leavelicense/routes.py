from flask import render_template, flash, redirect,request, Markup, url_for, abort
from . import bp

from .forms import LeaveLicensePersonalCreateForm, LeaveLicenseDesignationCreateForm

from sileg.auth import require_user
from sileg.models import usersModel, open_users_session, silegModel, open_sileg_session

from sileg_model.model.entities.Designation import DesignationTypes

def dt2s(dt: DesignationTypes):
    if dt == DesignationTypes.ORIGINAL:
        return 'Original'
    if dt == DesignationTypes.EXTENSION:
        return 'Prorroga'
    if dt == DesignationTypes.PROMOTION:
        return 'Extensión'
    if dt == DesignationTypes.REPLACEMENT:
        return 'Suplencia'
    return ''

@bp.route('/personal/<uid>')
@require_user
def create_personal_leave(user, uid):
    """
        Pagina de creacion de Licencia Personal
    """
    assert uid is not None
    with open_users_session() as session:
        person = usersModel.get_users(session, uids=[uid])[0]
    form = LeaveLicensePersonalCreateForm()
    return render_template('createPersonalLeaveLicense.html', user=user, person=person, form=form)

@bp.route('/personal/<uid>', methods=['POST'])
@require_user
def create_personal_leave_post(user, uid):
    """
        Pagina de creacion de Licencia Personal
    """
    assert uid is not None
    with open_sileg_session() as session:
        form = LeaveLicensePersonalCreateForm()

        if not form.validate_on_submit():
            print(form.errors)
            abort(404)

        form.save(session, silegModel, uid)
        session.commit()

    return redirect(url_for('designations.personDesignations', dt2s=dt2s, uid=uid))

@bp.route('/designacion/crear')
@require_user
def createDesignationLeave(user):
    """
    Pagina de creacion de Licencia de Designacion
    """
    form = LeaveLicenseDesignationCreateForm()
    person = {
        'dni': '12345678',
        'firstname': 'Pablo',
        'lastname': 'Rey'
    }
    return render_template('createDesignationLeaveLicense.html', user=user, person=person, form=form)

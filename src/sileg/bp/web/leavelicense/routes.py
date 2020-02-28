from flask import render_template, flash, redirect,request, Markup, url_for, abort
from . import bp

from .forms import LeaveLicensePersonalCreateForm, DesignationLeaveLicenseCreateForm
from .forms import lt2s

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


@bp.route('<uid>')
@require_user
def list_leave_licenses(user, uid):
    """
        Pagina de creacion de Licencia Personal
    """
    assert uid is not None
    with open_users_session() as session:
        person = usersModel.get_users(session, uids=[uid])[0]

    with open_sileg_session() as session:
        lids = silegModel.get_user_licenses(session, uid)
        plicenses = silegModel.get_ulicenses(session, lids=lids)

        lids = silegModel.get_user_designation_licenses(session, uid)
        licenses = silegModel.get_dlicenses(session, lids=lids)

        return render_template('personLicenses.html', user=user, person=person, lt2s=lt2s, plicenses=plicenses, licenses=licenses)

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

    return redirect(url_for('designations.personDesignations', uid=uid))

@bp.route('/designacion/<did>')
@require_user
def create_designation_leave_license(user, did):
    """
    Pagina de creacion de Licencia de Designacion
    """
    assert did is not None
    
    with open_sileg_session() as session:
        designations = silegModel.get_designations(session, [did])
        if not designations or len(designations) <= 0:
            abort(404)

        designation = designations[0]
        uid = designation.user_id
        with open_users_session() as usession:
            person = usersModel.get_users(usession, [uid])[0]

            form = DesignationLeaveLicenseCreateForm()
            return render_template('createDesignationLeaveLicense.html', user=user, person=person, designation=designation, form=form)

@bp.route('/designacion/<did>', methods=['POST'])
@require_user
def create_designation_leave_license_post(user, did):
    assert did is not None
    with open_sileg_session() as session:
        uid = silegModel.get_designations(session, [did])[0].user_id
        
        form = DesignationLeaveLicenseCreateForm()

        if not form.validate_on_submit():
            print(form.errors)
            abort(404)

        form.save(session, silegModel, did)
        session.commit()

    return redirect(url_for('designations.personDesignations', uid=uid))    
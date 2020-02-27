import base64
import mimetypes
import io
from flask import render_template, flash, redirect,request, Markup, url_for, abort, send_file
from . import bp

from .forms import PersonCreateForm, PersonSearchForm, DegreeAssignForm, PersonModifyForm

from sileg.helpers.namesHandler import id2sDegrees

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
        identityNumber = form.save(user['sub'])
        if identityNumber:
            return redirect(url_for('persons.search', query=identityNumber))
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
    else:
        persons = None
    return render_template('searchPerson.html', user=user, persons=persons, form=form)


@bp.route('<uid>/titulos',methods=['GET','POST'])
@require_user
def degrees(user,uid):
    """
    Pagina de Listado de Títulos de persona
    """
    form = DegreeAssignForm()
    with open_users_session() as session:
        persons = usersModel.get_users(session, [uid])
        if not persons or len(persons) <= 0:
            abort(404)
        person = persons[0]
        degrees = usersModel.get_person_degrees(session,uid)
        if degrees:
            for d in degrees:
                d.type = id2sDegrees(d.type)
    if form.validate_on_submit():
        form.save(uid,user['sub'])
        return redirect(url_for('persons.degrees', uid=uid))
    return render_template('showDegrees.html', user=user,person=person, degrees=degrees, form=form)


@bp.route('<uid>/titulos/<did>/eliminar')
@require_user
def deleteDegree(user,uid,did):
    """
    Metodo de baja de titulo
    """
    with open_users_session() as session:
        degree = usersModel.delete_person_degree(session,uid,did,user['sub'])
        if not degree:
            abort(404)
        elif degree == did:
            session.commit()
        return redirect(url_for('persons.degrees', uid=uid))

@bp.route('<uid>/titulos/<did>/descargar')
@require_user
def downloadDegree(user,uid,did):
    with open_users_session() as session:
        person = usersModel.get_users(session,[uid])[0]
        degree = usersModel.get_person_degree(session,uid,did)
        if degree and degree.file_id is not None:
            fid = degree.file_id
            data = usersModel.get_file(session, fid)
            content = data.content
            binary = base64.b64decode(content.encode())
            extension = mimetypes.guess_extension(data.mimetype)
            if degree.title:
                fileName = (person.lastname + degree.title + extension).replace(' ','')
            else:
                fileName = (person.lastname + extension).replace(' ','')
            return send_file(io.BytesIO(binary), attachment_filename=fileName, as_attachment=True ,mimetype=data.mimetype)
        return redirect(url_for('persons.degrees', uid=uid))

@bp.route('<uid>')
@require_user
def personData(user,uid):
    """
    Pagina de vista de datos personales
    """
    with open_users_session() as session:
        persons = usersModel.get_users(session, [uid])
        if not persons or len(persons) <= 0:
            abort(404)
        person = persons[0]
        #for pi in person.identity_numbers:
        #    pi.file
        return render_template('showPerson.html', user=user,person=person)

@bp.route('<uid>/documento/<iid>/descargar')
@require_user
def downloadIdNumberFile(user,uid,iid):
    with open_users_session() as session:
        person = usersModel.get_users(session,[uid])[0]
        identityNumber = usersModel.get_person_identityNumber(session,uid,iid)
        if identityNumber and identityNumber.file_id is not None:
            data = usersModel.get_file(session,identityNumber.file_id)
            content = data.content
            binary = base64.b64decode(content.encode())
            extension = mimetypes.guess_extension(data.mimetype)
            fileName = (person.lastname + identityNumber.type.value + extension).replace(' ','')
            return send_file(io.BytesIO(binary), attachment_filename=fileName, as_attachment=True ,mimetype=data.mimetype)
        return redirect(url_for('persons.personData', uid=uid))

@bp.route('<uid>/modificar')
@require_user
def modifyPersonData(user,uid):
    """
    Pagina de vista de datos personales
    """
    with open_users_session() as session:
        persons = usersModel.get_users(session, [uid])
        if not persons or len(persons) <= 0:
            abort(404)
        person = persons[0]
        form = PersonModifyForm()
        if person.lastname:
            form.lastname.data = person.lastname
        if person.firstname:
            form.firstname.data = person.firstname
        if person.gender:
            form.gender.data = person.gender
        if person.marital_status:
            form.marital_status.data = person.marital_status
        if person.birthplace:
            form.birthplace.data = person.birthplace
        if person.birthdate:
            form.birthdate.data = person.birthdate.strftime('%d/%m/%Y')
        if person.address:
            form.address.data = person.address
        if person.residence:
            form.residence.data = person.residence
        if len(person.mails) > 0:
            for pm in person.mails: 
                if pm.type.value == 'INSTITUTIONAL':
                    form.work_email.data = pm.email
                if pm.type.value == 'ALTERNATIVE':
                    form.personal_email.data = pm.email
        if len(person.phones) > 0:
            for ph in person.phones:
                if ph.type.value == 'LANDLINE':
                    form.land_line.data = ph.number
                if ph.type.value == 'CELLPHONE':
                    form.mobile_number.data = ph.number
        if form.validate_on_submit():
            form.save(user['sub'])

    return render_template('modifyPerson.html', user=user, person=person, form=form)
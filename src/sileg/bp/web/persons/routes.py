import base64
import mimetypes
import io
from flask import render_template, flash, redirect,request, Markup, url_for, abort, send_file
from . import bp

from .forms import PersonCreateForm, PersonSearchForm, DegreeAssignForm, PersonDataModifyForm, PersonIdNumberModifyForm, PersonMailModifyForm, PersonPhoneModifyForm, PersonSeniorityModifyForm

from sileg.helpers.namesHandler import id2sDegrees

from sileg.auth import require_user

from sileg.auth import oidc
from sileg.models import usersModel, open_users_session, silegModel, open_sileg_session


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
            flash(Markup('<span>¡Usuario Creado!</span>'))
            return redirect(url_for('persons.search', query=identityNumber))
        else:
            flash(Markup('<span>¡Error al crear el usuario!, intente nuevamente.</span>'))
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
    search = []
    if query:
        with open_users_session() as session:
            uids = usersModel.search_user(session, query)
            #Filtro uids repetidos
            for uid in uids:
                if uid not in search:
                    search.append(uid)
            persons = usersModel.get_users(session, search)
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
            flash(Markup('<span>¡Error al eliminar el titulo!</span>'))
            abort(404)
        elif degree == did:
            flash(Markup('<span>¡Titulo eliminado!</span>'))
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
        if not persons or len(persons) <= 0 or persons[0].deleted:
            abort(404)
        person = persons[0]
        external_seniority = None
        with open_sileg_session() as sileg_session:
            es_id = silegModel.get_external_seniority_by_user(sileg_session, uid)
            if es_id:
                es = silegModel.get_external_seniority(sileg_session, es_id)
                if es and len(es) >= 1 and not es[0].deleted:
                    external_seniority = es[0]
        return render_template('showPerson.html', user=user,person=person,external_seniority=external_seniority)

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

@bp.route('<uid>/modificar',methods=['GET','POST'])
@require_user
def modifyPersonData(user,uid):
    """
    Pagina de modificacion de datos personales
    """
    with open_users_session() as session:
        persons = usersModel.get_users(session, [uid])
        if not persons or len(persons) <= 0:
            if persons[0].deleted:
                abort(404)
        person = persons[0]
        formModifyPersonData = PersonDataModifyForm()
        formModifyIdNumber = PersonIdNumberModifyForm()
        formModifyMail = PersonMailModifyForm()
        formModifyPhone = PersonPhoneModifyForm()
        formModifySeniority = PersonSeniorityModifyForm()
        
        ### formModifyPersonData ###
        if person.lastname:
            formModifyPersonData.lastname.data = person.lastname
        if person.firstname:
            formModifyPersonData.firstname.data = person.firstname        
        if person.gender:
            formModifyPersonData.gender.data = person.gender
        if person.marital_status:
            formModifyPersonData.marital_status.data = person.marital_status
        if person.birthplace:
            formModifyPersonData.birthplace.data = person.birthplace
        if person.birthdate:
            formModifyPersonData.birthdate.data = person.birthdate.strftime('%d-%m-%Y')
        if person.address:
            formModifyPersonData.address.data = person.address
        if person.residence:
            formModifyPersonData.residence.data = person.residence
        if formModifyPersonData.personDataModify.data and (formModifyPersonData.residence.data != formModifyPersonData.residence.raw_data[0] or formModifyPersonData.lastname.data != formModifyPersonData.lastname.raw_data[0] or formModifyPersonData.firstname.data != formModifyPersonData.firstname.raw_data[0] or formModifyPersonData.gender.data != formModifyPersonData.gender.raw_data[0] or formModifyPersonData.marital_status.data != formModifyPersonData.marital_status.raw_data[0] or formModifyPersonData.birthplace.data != formModifyPersonData.birthplace.raw_data[0] or formModifyPersonData.birthdate.data != formModifyPersonData.birthdate.raw_data[0] or formModifyPersonData.address.data != formModifyPersonData.address.raw_data[0]):
            if formModifyPersonData.validate_on_submit():
                message = formModifyPersonData.saveModifyPersonData(person.id,user['sub'])
                flash(message)
                return redirect(url_for('persons.modifyPersonData', uid=uid))
        
        ### formModifyIdNumber
        if len(person.identity_numbers) > 0:
           for pi in person.identity_numbers:
               if not pi.deleted:
                   if pi.type.value != 'PASSPORT':
                       formModifyIdNumber.person_number_type.choices.remove((pi.type.value,pi.type.value))
                   else:
                       formModifyIdNumber.person_number_type.choices.remove((pi.type.value,'Pasaporte'))
        if 'idNumber' in request.form:
            if formModifyIdNumber.validate_on_submit():
                message = formModifyIdNumber.saveModifyIdNumber(person.id,user['sub'])
                flash(message)
                return redirect(url_for('persons.modifyPersonData', uid=uid))

        ### formModifyMail
        if len(person.mails) > 0:
            for pm in person.mails:
                if not pm.deleted:
                    if pm.type.value == 'INSTITUTIONAL':
                        formModifyMail.email_type.choices.remove((pm.type.value,'Institucional'))
        if 'mail' in request.form:
            if formModifyMail.validate_on_submit():
                message = formModifyMail.saveModifyMail(person.id,user['sub'])
                flash(message)
                return redirect(url_for('persons.modifyPersonData', uid=uid))

        ### formModifyPhone
        if 'phone' in request.form:
            if formModifyPhone.validate_on_submit():
                message = formModifyPhone.saveModifyPhone(person.id,user['sub'])
                flash(message)
                return redirect(url_for('persons.modifyPersonData', uid=uid))

    return render_template('modifyPerson.html', user=user, person=person, formModifyPersonData=formModifyPersonData, formModifyIdNumber=formModifyIdNumber, formModifyMail=formModifyMail, formModifyPhone=formModifyPhone, formModifySeniority=formModifySeniority)

@bp.route('<uid>/documento/<pidnumberid>/eliminar')
@require_user
def deleteIdentityNumber(user,uid,pidnumberid):
    """
    Metodo de baja de documento
    """
    with open_users_session() as session:
        identityNumber = usersModel.delete_person_idnumber(session,uid,pidnumberid,user['sub'])
        if not identityNumber:
            abort(404)
        elif identityNumber == pidnumberid:
            session.commit()
            flash('Documento eliminado correctamente')
        else:
            flash('Error interno')
        return redirect(url_for('persons.modifyPersonData', uid=uid))

@bp.route('<uid>/correo/<pmid>/eliminar')
@require_user
def deleteMail(user,uid,pmid):
    """
    Metodo de baja de email
    """
    with open_users_session() as session:
        mail = usersModel.delete_person_mail(session,uid,pmid,user['sub'])
        if not mail:
            abort(404)
        elif mail == pmid:
            session.commit()
            flash('Correo eliminado correctamente')
        else:
            flash('Error interno')
        return redirect(url_for('persons.modifyPersonData', uid=uid))

@bp.route('<uid>/telefono/<phid>/eliminar')
@require_user
def deletePhone(user,uid,phid):
    """
    Metodo de baja de teléfono
    """
    with open_users_session() as session:
        phone = usersModel.delete_person_phone(session,uid,phid,user['sub'])
        if not phone:
            abort(404)
        elif phone == phid:
            session.commit()
            flash('Teléfono eliminado correctamente')
        else:
            flash('Error interno')
        return redirect(url_for('persons.modifyPersonData', uid=uid))
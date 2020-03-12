import base64
import mimetypes
import io
from flask import render_template, flash, redirect,request, Markup, url_for, abort, send_file
from . import bp

from .forms import StudentCreateForm, StudentDataModifyForm, StudentIdNumberModifyForm

from sileg.helpers.namesHandler import id2sDegrees

from sileg.auth import require_user

from sileg.auth import oidc
from sileg.models import usersModel, open_users_session


@bp.route('/crear',methods=['GET','POST'])
@require_user
def create(user):
    """
    Pagina principal de estudiantes
    """
    form = StudentCreateForm()
    if form.validate_on_submit():
        identityNumber = form.save(user['sub'])
        if identityNumber:
            flash(Markup('<span>¡Estudiante Creado!</span>'))
            return redirect(url_for('persons.search', query=identityNumber))
        else:
            flash(Markup('<span>¡Error al crear el usuario!, intente nuevamente.</span>'))
    return render_template('createStudent.html', user=user, form=form)

@bp.route('<uid>/modificar',methods=['GET','POST'])
@require_user
def modifyStudentData(user,uid):
    """
    Pagina de modificacion de datos personales
    """
    with open_users_session() as session:
        persons = usersModel.get_users(session, [uid])
        if not persons or len(persons) <= 0:
            if persons[0].deleted:
                abort(404)
        person = persons[0]
        formModifyPersonData = StudentDataModifyForm()
        formModifyIdNumber = StudentIdNumberModifyForm()
        
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

    return render_template('modifyStudent.html', user=user, person=person, formModifyPersonData=formModifyPersonData, formModifyIdNumber=formModifyIdNumber, formModifyMail=formModifyMail, formModifyPhone=formModifyPhone, formModifySeniority=formModifySeniority)

from flask import render_template, flash, redirect,request, Markup, url_for, abort, send_file
from . import bp

from .forms import StudentCreateForm, StudentCSVCreateForm
from sileg.helpers.namesHandler import id2sDegrees

from sileg.auth import require_user

from sileg.helpers.permissionsHelper import verify_admin_permissions, verify_sileg_permission, verify_students_permission

from sileg.auth import oidc
from sileg.models import usersModel, open_users_session

@bp.route('/crear')
@require_user
@verify_students_permission
def create(user):
    """
    Pagina de creacion de alumnos GET
    """
    form = StudentCreateForm()
    return render_template('createStudent.html',user=user,form=form)

@bp.route('/crear',methods=['POST'])
@require_user
@verify_students_permission
def create_post(user):
    """
    Pagina de creacion de alumnos POST
    """
    form = StudentCreateForm()
    if form.validate_on_submit():
        identityNumber = form.save(user['sub'])
        if identityNumber:
            flash(Markup('<span>¡Alumno Creado!</span>'))
            return redirect(url_for('persons.search', query=identityNumber))
        else:
            flash(Markup('<span>¡Error al crear el alumno!, intente nuevamente.</span>'))
    return render_template('createStudent.html', user=user, form=form)

@bp.route('/cargar')
@require_user
@verify_students_permission
def loadFile(user):
    """
    Pagina de carga de csv
    """
    form = StudentCSVCreateForm()
    return render_template('loadFile.html',user=user,form=form)

@bp.route('/cargar', methods=['POST'])
@require_user
@verify_students_permission
def processFile(user):
    """
    Pagina de procesamiento de CSV
    """
    form = StudentCSVCreateForm()
    response = None
    count = {}
    if form.validate_on_submit():       
        response = form.save(user['sub'])
        count = {
            'total': len(response),
            'correct': len([r for r in response if r['status'] == 'Creado Correctamente']),
            'errors': len([r for r in response if r['status'] != 'Creado Correctamente'])
        }
    return render_template('creationResponse.html',user=user,response=response, count=count)
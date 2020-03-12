import base64
import mimetypes
import io
from flask import render_template, flash, redirect,request, Markup, url_for, abort, send_file
from . import bp

from .forms import StudentCreateForm
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

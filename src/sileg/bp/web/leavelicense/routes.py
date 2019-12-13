from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp

from .forms import LeaveLicensePersonalCreateForm, LeaveLicenseDesignationCreateForm

from sileg.auth import require_user

@bp.route('/personal/crear')
@require_user
def createPersonalLeave(user):
    """
    Pagina de creacion de Licencia Personal
    """
    form = LeaveLicensePersonalCreateForm()
    person = {
        'dni': '12345678',
        'firstname': 'Pablo',
        'lastname': 'Rey'
    }
    return render_template('createPersonalLeaveLicense.html', user=user, person=person, form=form)


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

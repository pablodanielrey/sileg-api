from flask import render_template, flash, redirect,request, Markup, url_for

from .forms import LeaveLicensePersonalCreateForm, LeaveLicenseDesignationCreateForm

from . import bp

@bp.route('/personal/crear')
def createPersonalLeave():
    """
    Pagina de creacion de Licencia Personal
    """
    form = LeaveLicensePersonalCreateForm()
    user = {
        'dni': '12345678',
        'firstname': 'Pablo',
        'lastname': 'Rey'
    }
    return render_template('createPersonalLeaveLicense.html', user=user, form=form)


@bp.route('/designacion/crear')
def createDesignationLeave():
    """
    Pagina de creacion de Licencia de Designacion
    """
    form = LeaveLicenseDesignationCreateForm()
    user = {
        'dni': '12345678',
        'firstname': 'Pablo',
        'lastname': 'Rey'
    }
    return render_template('createDesignationLeaveLicense.html', user=user, form=form)

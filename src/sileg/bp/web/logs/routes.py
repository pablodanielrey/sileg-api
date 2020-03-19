from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp

from sileg.auth import require_user

from sileg.helpers.permissionsHelper import verify_admin_permissions, verify_sileg_permission, verify_students_permission

from sileg.models import usersModel, open_users_session, silegModel, open_sileg_session

def _find_user(uid):
    fullname = 'Systema'
    #with open_users_session() as session:
    #    user = usersModel.get_users(session,[uid])[0]
    #if user:
    #    fullname = f'{user.lastname}, {user.firstname}'
    return uid

@bp.route('/usuarios')
@require_user
@verify_admin_permissions
def listUserLogs(user):
    """
    Pagina de listado de logs de usuarios
    """
    logs = []
    with open_users_session() as session:
        logs = usersModel.get_logs(session, 100)
    return render_template('listUserLogs.html',user=user, logs=logs,_find_user=_find_user)

@bp.route('/sileg')
@require_user
@verify_admin_permissions
def listSilegLogs(user):
    """
    Pagina de listado de logs de Sileg
    """
    logs = []
    with open_sileg_session() as session:
        logs = silegModel.get_logs(session, 100)
    return render_template('listSilegLogs.html',user=user,logs=logs,_find_user=_find_user)

@bp.route('<lid>/detail')
@require_user
@verify_admin_permissions
def logDetail(user,lid):
    """
    Pagina de detalle de un log
    """
    assert lid is not None
    with open_sileg_session() as session:
        log = silegModel.get_log(session, lid)
    if not log:
        with open_users_session() as session2:
            log = usersModel.get_log(session2, lid)
    return render_template('logDetail.html',user=user,log=log)

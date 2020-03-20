import json

from flask import render_template, flash, redirect,request, Markup, url_for
from . import bp

from sileg.auth import require_user

from sileg.helpers.permissionsHelper import verify_admin_permissions, verify_sileg_permission, verify_students_permission

from sileg.models import usersModel, open_users_session, silegModel, open_sileg_session


@bp.route('/usuarios')
@require_user
@verify_sileg_permission
def listUserLogs(user):
    """
    Pagina de listado de logs de usuarios
    """
    logs = []
    with open_users_session() as session:
        logs = usersModel.get_logs(session, 100)
        uids = [l.authorizer_id for l in logs]
        uids = list(set(uids))
        try:
            users = usersModel.get_users(session, uids)
        except:
            users = []
    usersLogs = {}
    for user in users:
        usersLogs[user.id] = user
    return render_template('listUserLogs.html', user=user, usersLogs=usersLogs, logs=logs)

@bp.route('/sileg')
@require_user
@verify_sileg_permission
def listSilegLogs(user):
    """
    Pagina de listado de logs de Sileg
    """
    logs = []
    with open_sileg_session() as session:
        logs = silegModel.get_logs(session, 100)
    with open_users_session() as sessionU:
        uids = [l.authorizer_id for l in logs]
        uids = list(set(uids))
        try:
            users = usersModel.get_users(sessionU, uids)
        except:
            users = []
    usersLogs = {}
    for user in users:
        usersLogs[user.id] = user
    return render_template('listSilegLogs.html',user=user, usersLogs=usersLogs, logs=logs)

@bp.route('/users/<lid>/detail')
@require_user
@verify_admin_permissions
def usersLogDetail(user,lid):
    """
    Pagina de detalle de un log
    """
    assert lid is not None
    with open_users_session() as session:
        log = usersModel.get_log(session, lid)
        try:
            authorizer = usersModel.get_users(session, [log.authorizer_id])[0]
        except:
            authorizer = None
    campos = json.loads(log.data)
    return render_template('logDetail.html',user=user,authorizer=authorizer,log=log,campos=campos)

@bp.route('/sileg/<lid>/detail')
@require_user
@verify_admin_permissions
def silegLogDetail(user,lid):
    """
    Pagina de detalle de un log
    """
    assert lid is not None
    with open_sileg_session() as session:
        log = silegModel.get_log(session, lid)
    with open_users_session() as sessionU:
        try:
            authorizer = usersModel.get_users(sessionU, [log.authorizer_id])[0]
        except:
            authorizer = None
    campos = json.loads(log.data)
    return render_template('logDetail.html',user=user,authorizer=authorizer,log=log,campos=campos)

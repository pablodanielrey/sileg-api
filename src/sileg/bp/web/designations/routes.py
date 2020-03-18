import json
from flask import render_template, flash, redirect,request, Markup, url_for, abort

from sileg.auth import require_user
from sileg.models import silegModel, open_sileg_session, usersModel, open_users_session
from sileg_model.model.entities.Designation import Designation, DesignationTypes, DesignationEndTypes
from sileg_model.model.entities.Place import PlaceTypes
from sileg_model.model.entities.Log import SilegLog, SilegLogTypes

from sileg.helpers.permissionsHelper import verify_admin_permissions, verify_sileg_permission, verify_students_permission

from . import bp
from .forms import ExtendDesignationForm, \
                DesignationCreateForm, \
                ReplacementDesignationCreateForm, \
                ConvalidateDesignationForm, \
                PromoteDesignationForm, \
                ExtendDesignationForm, \
                DischargeDesignationForm, \
                DeleteDesignationForm, \
                DesignationSearchForm, \
                PersonSearchForm 


"""
    //////////////////////////////////////////////////////////////////////
        FUNCIONES AUXILIARES USADAS EN LAS VISTAS
    //////////////////////////////////////////////////////////////////////
"""

def calculate_end(d:Designation):
    if d.deleted:
        return None
    end = d.end
    if d.designations:
        for d2 in d.designations:
            if not d2.deleted:
                if not end or (d2.type is DesignationTypes.EXTENSION and d2.end and d2.end > end):
                    end = d2.end
    return end

def det2s(det: DesignationEndTypes):
    if det == DesignationEndTypes.INDETERMINATE:
        return 'Indeterminado'
    if det == DesignationEndTypes.REPLACEMENT:
        return 'Hasta fin de suplencia'
    if det == DesignationEndTypes.CONTEST:
        return 'Hasta concurso'
    if det == DesignationEndTypes.CONVALIDATION:
        return 'Hasta convalidación por consejo superior'
    if det == DesignationEndTypes.ENDDATE:
        return 'Hasta fecha fin'
    if det == DesignationEndTypes.RENEWAL:
        return 'Hasta nuevo llamado'
    return ''

def dt2s(dt: DesignationTypes):
    if dt == DesignationTypes.ORIGINAL:
        return 'Original'
    if dt == DesignationTypes.EXTENSION:
        return 'Prorroga'
    if dt == DesignationTypes.PROMOTION:
        return 'Extensión'
    if dt == DesignationTypes.REPLACEMENT:
        return 'Suplencia'
    if dt == DesignationTypes.DISCHARGE:
        return 'Baja'
    return ''

def placeTypeToString(p:PlaceTypes):
    if p == PlaceTypes.UNIVERSIDAD:
        return 'Universidad'
    if p == PlaceTypes.FACULTAD:
        return 'Facultad'
    if p == PlaceTypes.SECRETARIA:
        return 'Secretaría'
    if p == PlaceTypes.PROSECRETARIA:
        return 'Pro-Secretaría'
    if p == PlaceTypes.DEPARTAMENTO:
        return 'Departamento'
    if p == PlaceTypes.DIRECCION:
        return 'Dirección'
    if p == PlaceTypes.INSTITUTO:
        return 'Instituto'
    if p == PlaceTypes.ESCUELA:
        return 'Escuela'
    if p == PlaceTypes.SEMINARIO:
        return 'Seminario'
    if p == PlaceTypes.AREA:
        return 'Area'
    if p == PlaceTypes.DIVISION:
        return 'División'
    if p == PlaceTypes.MAESTRIA:
        return 'Maestría'
    if p == PlaceTypes.CENTRO:
        return 'Centro'
    if p == PlaceTypes.MATERIA:
        return 'Materia'
    if p == PlaceTypes.CATEDRA:
        return 'Catedra'



def _is_extension(d):
    return d.type == DesignationTypes.EXTENSION

def _is_promotion(d):
    return d.type == DesignationTypes.PROMOTION

def _is_secondary(d:Designation):
    """ 
        retorna true si va en el listado secundario de desiganciones
        ej: bajas de prorrogas, prorrogas
    """
    if d.type == DesignationTypes.DISCHARGE:
        return d.designation.type == DesignationTypes.EXTENSION
    return d.type == DesignationTypes.EXTENSION

def _is_suplencia(d:Designation):
    return d.type == DesignationTypes.REPLACEMENT

def _has_suplencia(ls:[]):
    for l in ls:
        if _is_suplencia(l):
            return True
    return False

def _has_extension(ls:[]):
    for l in ls:
        if _is_extension(l):
            return True
    return False

def _find_user(d:Designation):
    uid = d.user_id
    fullname = ''
    with open_users_session() as session:
        user = usersModel.get_users(session,[uid])[0]
    if user:
        fullname = f'{user.lastname}, {user.firstname}'
    return fullname


"""
    ############################################
    ####################### SUPLENCIAS ##########################
    ############################################
"""


@bp.route('/suplencia_seleccionar_persona/<did>')
@require_user
@verify_sileg_permission
def replacement_select_person(user, did):
    """
        Paso 1 de generación de una suplencia.
        se selecciona la persona de reemplazo
    """
    assert did is not None

    form = PersonSearchForm()
    query = request.args.get('query','',str)
    persons = []
    if query:
        with open_users_session() as session:
            uids = usersModel.search_user(session, query)
            persons = usersModel.get_users(session, uids)
    else:
        persons = None
    return render_template('generateReplacement1.html', user=user, persons=persons, did=did, form=form)

@bp.route('/suplencia_crear/<did>/<uid>')
@require_user
@verify_sileg_permission
def replacement_create_designation(user, did, uid):
    """
        Paso 2 de generación de una suplencia.
        genero la designacion como suplencia.
    """
    assert did is not None
    assert uid is not None

    with open_sileg_session() as session:
        form = ReplacementDesignationCreateForm(session, silegModel)
        designation = silegModel.get_designations(session, [did])[0]

        original_uid = designation.user_id

        with open_users_session() as session:
            person = usersModel.get_users(session, uids=[original_uid])[0]
            replacement = usersModel.get_users(session, uids=[uid])[0]

        return render_template('generateReplacement2.html', user=user, person=person, replacement=replacement, designation=designation, form=form)

@bp.route('/suplencia_crear/<did>/<uid>', methods=['POST'])
@require_user
@verify_sileg_permission
def replacement_create_designation_post(user, did, uid):
    """
        post del formulario con los datos completos para generar la suplencia.
    """
    assert did is not None
    assert uid is not None

    with open_sileg_session() as session:
        form = ReplacementDesignationCreateForm(session, silegModel)
        original_designation = silegModel.get_designations(session, [did])[0]
        original_uid = original_designation.user_id

        if not form.is_submitted():
            flash(Markup('<span>¡Error en la creación de suplencia!</span>'))
            print(form.errors)
            abort(404)

        form.save(session, silegModel, uid, did, user['sub'])
        session.commit()
        flash(Markup('<span>¡Suplencia Creada!</span>'))

    return redirect(url_for('designations.personDesignations', uid=original_uid))
    

"""
    ##################################################
    ############ Convalidación por consejo ###########
    ##################################################
"""

@bp.route('/convalidar/<did>')
@require_user
@verify_sileg_permission
def convalidate(user, did):
    """
        Paso 1 de generación de una convalidación
        genero la designacion nueva
    """
    assert did is not None

    with open_sileg_session() as session:
        form = ConvalidateDesignationForm(session, silegModel)
        designation = silegModel.get_designations(session, [did])[0]
        original_uid = designation.user_id

        with open_users_session() as session:
            person = usersModel.get_users(session, uids=[original_uid])[0]

        return render_template('convalidateDesignation.html', user=user, person=person, designation=designation, form=form)
   

@bp.route('/convalidar/<did>', methods=['POST'])
@require_user
@verify_sileg_permission
def convalidate_post(user, did):
    """
        Metodo post de generacion de convalidacion
    """

    assert user is not None
    assert did is not None

    with open_sileg_session() as session:
        form = ConvalidateDesignationForm(session, silegModel)
        original_designation = silegModel.get_designations(session, [did])[0]
        uid = original_designation.user_id

        if not form.is_submitted():
            flash(Markup('<span>¡Error al crear convalidación!</span>'))
            print(form.errors)
            abort(404)

        form.save(session, original_designation, user['sub'])
        session.commit()
        flash(Markup('<span>¡Convalidación Creada!</span>'))

    return redirect(url_for('designations.personDesignations', uid=uid))

"""
    ##################################################
    ########### Extensión ##################
    ##################################################
"""

@bp.route('/extension/<did>')
@require_user
@verify_sileg_permission
def promote(user, did):
    """
        Paso 1 de generación de una extensión
        genero la designacion nueva
    """
    assert did is not None

    with open_sileg_session() as session:
        form = PromoteDesignationForm(session, silegModel)
        designation = silegModel.get_designations(session, [did])[0]
        original_uid = designation.user_id

        with open_users_session() as session:
            person = usersModel.get_users(session, uids=[original_uid])[0]

        return render_template('promoteDesignation.html', user=user, person=person, designation=designation, form=form)

@bp.route('/extension/<did>', methods=['POST'])
@require_user
@verify_sileg_permission
def promote_post(user, did):
    """
        Paso 2 de generación de una extensión
        se guardan los datos en la base
    """
    assert did is not None

    with open_sileg_session() as session:
        form = PromoteDesignationForm(session, silegModel)
        designation = silegModel.get_designations(session, [did])[0]
        uid = designation.user_id

        if not form.is_submitted():
            flash(Markup('<span>¡Error al crear extensión!</span>'))
            print(form.errors)
            abort(404)

        form.save(session, designation, user['sub'])
        session.commit()
        flash(Markup('<span>¡Extensión Creada!</span>'))

    return redirect(url_for('designations.personDesignations', uid=uid))

"""
    ########################################
    ########### PRORROGA ###########
    ########################################
"""

@bp.route('/prorroga/<did>')
@require_user
@verify_sileg_permission
def extend(user, did):
    """
        Paso 1 de generación de una prorroga
        genero la designacion nueva
    """
    assert did is not None

    with open_sileg_session() as session:
        form = ExtendDesignationForm(session, silegModel)
        designation = silegModel.get_designations(session, [did])[0]
        original_uid = designation.user_id

        with open_users_session() as session:
            person = usersModel.get_users(session, uids=[original_uid])[0]

        return render_template('extendDesignation.html', user=user, person=person, designation=designation, form=form)


@bp.route('/prorroga/<did>', methods=['POST'])
@require_user
@verify_sileg_permission
def extend_post(user, did):
    """
        Paso 2 de creacion de prorroga
        almaceno los datos en la base
    """
    assert did is not None

    with open_sileg_session() as session:
        form = ExtendDesignationForm(session, silegModel)
        designation = silegModel.get_designations(session, [did])[0]
        uid = designation.user_id

        if not form.is_submitted():
            flash(Markup('<span>¡Error al crear prórroga!</span>'))
            print(form.errors)
            abort(404)

        form.save(session, designation, user['sub'])
        session.commit()
        flash(Markup('<span>¡Prórroga Creada!</span>'))

    return redirect(url_for('designations.personDesignations', uid=uid))


"""
    ##########################################
    ################## BAJA ##################
    ##########################################
"""

@bp.route('/baja/<did>')
@require_user
@verify_sileg_permission
def discharge(user, did):
    """
        Crea una baja asociada a la designacion did
    """
    assert did is not None

    with open_sileg_session() as session:
        form = DischargeDesignationForm()
        designation = silegModel.get_designations(session, [did])[0]
        original_uid = designation.user_id

        with open_users_session() as session:
            person = usersModel.get_users(session, uids=[original_uid])[0]

        return render_template('dischargeDesignation.html', user=user, person=person, designation=designation, form=form)

@bp.route('/baja/<did>', methods=['POST'])
@require_user
@verify_sileg_permission
def discharge_post(user, did):
    """
        Genera la baja asociada a did, en la base de datos
    """
    assert did is not None

    with open_sileg_session() as session:
        form = DischargeDesignationForm()
        designation = silegModel.get_designations(session, [did])[0]
        uid = designation.user_id

        if not form.is_submitted():
            flash(Markup('<span>¡Error en la baja!</span>'))
            print(form.errors)
            abort(404)

        form.save(session, user['sub'], designation_to_discharge=designation)
        session.commit()
        flash(Markup('<span>¡Baja registrada correctamente!</span>'))

    return redirect(url_for('designations.personDesignations', uid=uid))



@bp.route('/restaurar/<did>')
@require_user
@verify_sileg_permission
def undelete(user, did):
    assert did is not None
    with open_sileg_session() as session:
        d = silegModel.get_designations(session, [did])[0]
        uid = d.user_id
        d.deleted = None
        d.historic = False
        
        undeleteToLog = {
            'id': d.id,
            'created': d.created,
            'updated': d.updated,
            'deleted': d.deleted,
            'start': d.start,
            'end': d.end,
            'end_type': d.end_type,
            'historic': d.historic,
            'exp': d.exp,
            'res': d.res,
            'cor': d.cor,
            'status': d.status,
            'type': d.type,
            'designation_id': d.designation_id,
            'user_id': d.user_id,
            'function_id': d.function_id,
            'place_id': d.place_id,
            'comments': d.comments,
        }
        log = SilegLog()
        log.type = SilegLogTypes.UPDATE
        log.entity_id = d.id
        log.authorizer_id = user['sub']
        log.data = json.dumps([undeleteToLog], default=str)
        session.add(log)

        session.commit()
        flash(Markup('<span>¡Designación Restaurada!</span>'))
    
    return redirect(url_for('designations.personDesignations', uid=uid))        


@bp.route('/eliminar/<did>')
@require_user
@verify_sileg_permission
def delete(user, did):
    """
        Confirmar la eliminación de la designación
    """
    assert did is not None

    with open_sileg_session() as session:
        form = DeleteDesignationForm()
        designation = silegModel.get_designations(session, [did])[0]
        original_uid = designation.user_id

        with open_users_session() as session:
            person = usersModel.get_users(session, uids=[original_uid])[0]

        return render_template('deleteDesignation.html', user=user, person=person, designation=designation, form=form)

@bp.route('/eliminar/<did>', methods=['POST'])
@require_user
@verify_sileg_permission
def delete_post(user, did):
    """
        Eliminación de la designación
    """
    assert did is not None

    with open_sileg_session() as session:
        form = DeleteDesignationForm()
        designation = silegModel.get_designations(session, [did])[0]
        uid = designation.user_id

        if not form.is_submitted():
            flash(Markup('<span>¡Error al eliminar designación!</span>'))
            print(form.errors)
            abort(404)

        form.save(session, designation, user['sub'])
        session.commit()
        flash(Markup('<span>¡Designación Eliminada!</span>'))

    return redirect(url_for('designations.personDesignations', uid=uid))


"""
    ########################################
"""


@bp.route('/detalle/<did>')
@require_user
@verify_sileg_permission
def designation_detail(user, did):
    """
        Detalle de una designación
    """
    assert did is not None

    with open_sileg_session() as session:
        designations = silegModel.get_designations(session, [did])
        designation = designations[0]
        uid = designation.user_id

        extensions = [d for d in designation.designations if d.type == DesignationTypes.EXTENSION]
        promotions = [d for d in designation.designations if d.type == DesignationTypes.PROMOTION]
        discharges = [d for d in designation.designations if d.type == DesignationTypes.DISCHARGE]

        #extensions = extensions.sort(reverse=True, key=lambda x:x.start)
        #promotions = promotions.sort(reverse=True, key=lambda x:x.start)
        if not extensions:
            extensions = []

        if not promotions:
            promotions = []

        with open_users_session() as session:
            person = usersModel.get_users(session, [uid])[0]

        return render_template('designationDetail.html', dt2s=dt2s, det2s=det2s, ie=_is_extension, ip=_is_promotion, user=user, person=person, designation=designation, extensions=extensions, promotions=promotions, discharges=discharges)


@bp.route('/listado/<uid>')
@require_user
@verify_sileg_permission
def personDesignations(user, uid):
    """
    Pagina de lisata de designaciones de una persona
    Recibe como parametro uid de la persona
    """
    assert uid is not None

    with open_users_session() as session:
        person = usersModel.get_users(session, [uid])[0]

    with open_sileg_session() as session:
        dids = silegModel.get_designations_by_uuid(session, uid)
        designations = silegModel.get_designations(session, dids)

        original = [d for d in designations if d.deleted is None and (d.type == DesignationTypes.ORIGINAL or d.type == DesignationTypes.REPLACEMENT)]

        #armo el grupo de las designaciones relacionadas con el cargo original
        active = []
        for d in original:
            related = [d]
            for dr in d.designations:
                if not (dr.historic or dr.deleted):
                    if dr.type is DesignationTypes.PROMOTION or dr.type is DesignationTypes.ORIGINAL:
                        related.append(dr)
            active.append(related)
        

        active = sorted(active, key=lambda d: d[0].start, reverse=True)

        return render_template('personDesignations.html', 
                    dt2s=dt2s, cend=calculate_end, user=user, 
                    designations=active, 
                    person=person, 
                    is_secondary=_is_secondary, 
                    is_suplencia=_is_suplencia, 
                    find_user=_find_user,
                    has_suplencia=_has_suplencia,
                    has_extension=_has_extension)

@bp.route('/cargo/<cid>')
@require_user
@verify_sileg_permission
def function_designations(user, cid):
    """
    Pagina de lista de designaciones por cargo
    """
    assert cid is not None

    with open_sileg_session() as session:
        function = silegModel.get_functions(session, [cid])[0]
        dids = silegModel.get_designations_by_functions(session, [cid])
        to_show = dids[:50]
        designations = silegModel.get_designations(session, to_show)
        original = [d for d in designations if d.deleted is None and not d.historic and (d.type == DesignationTypes.ORIGINAL or d.type == DesignationTypes.PROMOTION or d.type == DesignationTypes.REPLACEMENT)]
        original = sorted(original, key=lambda d:d.start, reverse=True)
        return render_template('functionDesignations.html', user=user, function=function, designations=original, dt2s=dt2s, cend=calculate_end, is_secondary=_is_secondary, is_suplencia=_is_suplencia, find_user=_find_user, placeTypeToString=placeTypeToString)


@bp.route('/lugar/<pid>')
@require_user
@verify_sileg_permission
def placeDesignations(user, pid):
    """
    Pagina de lisata de designaciones de un lugar
    Recibe como parametro pid del lugar
    """
    assert pid is not None

    with open_sileg_session() as session:
        place = silegModel.get_places(session,[pid])[0]
        dids = silegModel.get_designations_by_places(session, [pid])
        designations = silegModel.get_designations(session, dids)
        original = [d for d in designations if d.deleted is None and not d.historic and (d.type == DesignationTypes.ORIGINAL or d.type == DesignationTypes.REPLACEMENT)]

        persons_designations = {}

        #armo el grupo de las designaciones relacionadas con el cargo original
        active = []
        for d in original:
            related = [d]
            for dr in d.designations:
                if not (dr.historic or dr.deleted):
                    if dr.type is DesignationTypes.PROMOTION or dr.type is DesignationTypes.ORIGINAL:
                        related.append(dr)
            uid = related[0].user_id
            if uid not in persons_designations:
                persons_designations[uid] = []
            persons_designations[uid].append(related)

        for p in persons_designations.values():
            active.append(p)
        return render_template('placeDesignations.html', dt2s=dt2s, cend=calculate_end, user=user, persons=active, place=place, is_secondary=_is_secondary, is_suplencia=_is_suplencia, find_user=_find_user, placeTypeToString=placeTypeToString)


@bp.route('/crear/<uid>')
@require_user
@verify_sileg_permission
def create_get(user, uid):
    """
        Pagina de creacion de designacion
    """
    assert uid is not None

    with open_users_session() as session:
        person = usersModel.get_users(session, uids=[uid])[0]

    with open_sileg_session() as session:
        form = DesignationCreateForm(session, silegModel)
        #form._load_values(session, silegModel)
 
    return render_template('createDesignation.html', user=user, person=person, form=form)

@bp.route('/crear/<uid>', methods=['POST'])
@require_user
@verify_sileg_permission
def create_post(user, uid):
    """
        Pagina de creacion de designacion
    """
    assert uid is not None

    """
    with open_users_session() as session:
        person = usersModel.get_users(session, uids=[uid])[0]
    """

    with open_sileg_session() as session:
        form = DesignationCreateForm(session, silegModel)

        if not form.validate_on_submit():
            flash(Markup('<span>Error al crear designación!</span>'))
            print(form.errors)
            abort(404)

        form.save(session, silegModel, uid, user['sub'])
        session.commit()
        flash(Markup('<span>¡Designación Creada!</span>'))

    return redirect(url_for('designations.personDesignations', uid=uid))



from flask import render_template, flash, redirect,request, Markup, url_for, abort

from sileg.auth import require_user
from sileg.models import silegModel, open_sileg_session, usersModel, open_users_session
from sileg_model.model.entities.Designation import Designation, DesignationTypes, DesignationEndTypes

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


"""
    ############################################
    ####################### SUPLENCIAS ##########################
    ############################################
"""


@bp.route('/suplencia_seleccionar_persona/<did>')
@require_user
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
            print(form.errors)
            abort(404)

        form.save(session, silegModel, uid, did, user['sub'])
        session.commit()

    return redirect(url_for('designations.personDesignations', uid=original_uid))
    

"""
    ##################################################
    ############ Convalidación por consejo ###########
    ##################################################
"""

@bp.route('/convalidar/<did>')
@require_user
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
def convalidate_post(user, did):
    assert user is not None
    assert did is not None

    with open_sileg_session() as session:
        form = ConvalidateDesignationForm(session, silegModel)
        original_designation = silegModel.get_designations(session, [did])[0]
        uid = original_designation.user_id

        if not form.is_submitted():
            print(form.errors)
            abort(404)

        form.save(session, original_designation, user['sub'])
        session.commit()

    return redirect(url_for('designations.personDesignations', uid=uid))

"""
    ##################################################
    ########### Extensión ##################
    ##################################################
"""

@bp.route('/extension/<did>')
@require_user
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
            print(form.errors)
            abort(404)

        form.save(session, designation, user['sub'])
        session.commit()

    return redirect(url_for('designations.personDesignations', uid=uid))

"""
    ########################################
    ########### PRORROGA ###########
    ########################################
"""

@bp.route('/prorroga/<did>')
@require_user
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
            print(form.errors)
            abort(404)

        form.save(session, designation, user['sub'])
        session.commit()

    return redirect(url_for('designations.personDesignations', uid=uid))


"""
    ##########################################
    ################## BAJA ##################
    ##########################################
"""

@bp.route('/baja/<did>')
@require_user
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
            print(form.errors)
            abort(404)

        form.save(session, user['sub'], designation_to_discharge=designation)
        session.commit()

    return redirect(url_for('designations.personDesignations', uid=uid))



@bp.route('/restaurar/<did>')
@require_user
def undelete(user, did):
    assert did is not None
    with open_sileg_session() as session:
        d = silegModel.get_designations(session, [did])[0]
        uid = d.user_id
        d.deleted = None
        d.historic = False
        session.commit()
    
    return redirect(url_for('designations.personDesignations', uid=uid))        


@bp.route('/eliminar/<did>')
@require_user
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
            print(form.errors)
            abort(404)

        form.save(session, designation, user['sub'])
        session.commit()

    return redirect(url_for('designations.personDesignations', uid=uid))


"""
    ########################################
"""

def _is_extension(d):
    return d.type == DesignationTypes.EXTENSION

def _is_promotion(d):
    return d.type == DesignationTypes.PROMOTION

@bp.route('/detalle/<did>')
@require_user
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

def _find_user(d:Designation):
    uid = d.user_id
    fullname = ''
    with open_users_session() as session:
        user = usersModel.get_users(session,[uid])[0]
    if user:
        fullname = f'{user.lastname}, {user.firstname}'
    return fullname


@bp.route('/listado/<uid>')
@require_user
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

        return render_template('personDesignations.html', dt2s=dt2s, cend=calculate_end, user=user, designations=active, person=person, is_secondary=_is_secondary, is_suplencia=_is_suplencia, find_user=_find_user)


@bp.route('/crear/<uid>')
@require_user
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
            print(form.errors)
            abort(404)

        form.save(session, silegModel, uid, user['sub'])
        session.commit()

    return redirect(url_for('designations.personDesignations', uid=uid))


@bp.route('/buscar')
@require_user
def search(user):
    """
    Pagina de busqueda de desiganaciones
    """
    designations = [{
            'firstname':'Pablo',
            'lastname':'Rey',
            'place':'Ingles I',
            'placetype':'Original',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'A/D',
            'character': 'INT',
            'relatedTo': None
        },
        {
            'firstname':'Pablo',
            'lastname':'Rey',
            'place':'Seminario de Ingles',
            'placetype':'Original',
            'dedication': 'Exclusiva',
            'positionType': 'Cumpliendo funcion',
            'character': 'INT',
            'relatedTo': True
        },
        {
            'firstname':'Emanuel',
            'lastname':'Pais',
            'place':'Contabilidad III',
            'placetype':'Original',
            'dedication': 'Semi-dedicación',
            'observations': '-',
            'positionType': 'ADJ',
            'character': 'SUP',
            'relatedTo': None
        },
        {
            'firstname':'Miguel Angel Jesús',
            'lastname':'Macagno',
            'place':'Administración I',
            'placetype':'B',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'JAD',
            'character': 'INT',
            'relatedTo': None
        },
        {
            'firstname':'Leonardo',
            'lastname':'Consolini',
            'place':'Administración I',
            'placetype':'A',
            'dedication': 'Exclusiva',
            'observations': '-',
            'positionType': 'TIT',
            'character': 'INT',
            'relatedTo': None
        }
    ]
    form = DesignationSearchForm()
    return render_template('searchDesignations.html',user=user,designations=designations,form=form)




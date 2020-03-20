import datetime
import json
import uuid

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateTimeField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, EqualTo, Optional
#from wtforms.fields.html5 import DateTimeField

from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.Designation import Designation, DesignationTypes, DesignationEndTypes, DesignationStatus
from sileg_model.model.entities.Log import SilegLog, SilegLogTypes

def det2s(d: DesignationEndTypes):
    if d == DesignationEndTypes.INDETERMINATE:
        return 'Indeterminado'
    if d == DesignationEndTypes.CONVALIDATION:
        return 'Hasta Convalidación'
    if d == DesignationEndTypes.CONTEST:
        return 'Hasta Concurso'
    if d == DesignationEndTypes.RENEWAL:
        return 'Hasta Renovación'
    if d == DesignationEndTypes.REPLACEMENT:
        return 'Hasta Fin de Suplencia'
    if d == DesignationEndTypes.ENDDATE:
        return 'Fecha Fin'    

def ds2s(s:DesignationStatus):
    if s == DesignationStatus.APROVED:
        return 'Aprobada'
    if s == DesignationStatus.EFFECTIVE:
        return 'Efectivo'
    if s == DesignationStatus.PENDING:
        return 'Pendiente'
    if s == DesignationStatus.IMPORTED:
        return 'Importada'

class DesignationCreateForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    start = DateTimeField('Fecha Desde', format='%d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Fecha Hasta', format='%d-%m-%Y', validators=[Optional()])

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    status = SelectField('Estado', coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Suplente
    # aca hay que buscar alguna forma de seleccionar designaciones a las cual les realiza la suplencia.
    #replace = SelectField('Reemplaza a', coerce=str)

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session, silegModel.get_all_functions(session)) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [ (d.value, det2s(d)) for d in DesignationEndTypes ]
        self.status.choices = [(d.value, ds2s(d)) for d in DesignationStatus]
        
    def save(self, session, silegModel, uid, authorizer_id):
        d = Designation()
        d.id = str(uuid.uuid4())
        d.type = DesignationTypes.ORIGINAL
        d.user_id = uid

        d.start = self.start.data
        d.end = self.end.data
        d.function_id = self.function.data
        d.end_type = self.functionEndType.data
        d.place_id = self.place.data
        
        d.status = self.status.data

        d.comments = self.observations.data

        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        
        session.add(d)
                
        designationToLog = {
            'designation': {
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
                'comments': d.comments
            }
        }
        log = SilegLog()
        log.type = SilegLogTypes.CREATE
        log.entity_id = d.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([designationToLog], default=str)
        session.add(log)

class ReplacementDesignationCreateForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    start = DateTimeField('Fecha Desde', format='%d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Fecha Hasta', format='%d-%m-%Y', validators=[Optional()])

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session, silegModel.get_all_functions(session)) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [ (d.value, det2s(d)) for d in DesignationEndTypes ]
        
    def save(self, session, silegModel, uid, replaced_did, authorizer_id):
        d = Designation()
        d.id = str(uuid.uuid4())
        d.type = DesignationTypes.REPLACEMENT
        d.designation_id = replaced_did
        
        d.start = self.start.data
        d.end = self.end.data
        d.function_id = self.function.data
        d.end_type = self.functionEndType.data
        d.place_id = self.place.data
        d.user_id = uid
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        session.add(d)

        replacementToLog = {
            'designation': {
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
        }
        log = SilegLog()
        log.type = SilegLogTypes.CREATE
        log.entity_id = d.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([replacementToLog], default=str)
        session.add(log)

class ConvalidateDesignationForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    start = DateTimeField('Fecha Desde', format='%d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Fecha Hasta', format='%d-%m-%Y', validators=[Optional()])

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session, silegModel.get_all_functions(session)) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [ (d.value, det2s(d)) for d in DesignationEndTypes ]        

    def save(self, session, replaced_designation: Designation, authorizer_id):
        #replaced_designation.deleted = datetime.datetime.now()
        replaced_designation.historic = True

        d = Designation()
        d.id = str(uuid.uuid4())
        d.type = DesignationTypes.ORIGINAL
        d.designation_id = replaced_designation.id
        d.user_id = replaced_designation.user_id
        d.place_id = replaced_designation.place_id
        
        d.start = self.start.data
        d.end = self.end.data
        d.function_id = self.function.data
        d.end_type = self.functionEndType.data
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        session.add(d)

        convalidateToLog = {
            'designation': {
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
        }
        log = SilegLog()
        log.type = SilegLogTypes.CREATE
        log.entity_id = d.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([convalidateToLog], default=str)
        session.add(log)


class PromoteDesignationForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    start = DateTimeField('Fecha Desde', format='%d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Fecha Hasta', format='%d-%m-%Y',  validators=[Optional()])

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session, silegModel.get_all_functions(session)) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [ (d.value, det2s(d)) for d in DesignationEndTypes ]
        
    def save(self, session, designation: Designation, authorizer_id):
        d = Designation()
        d.id = str(uuid.uuid4())
        d.type = DesignationTypes.PROMOTION
        d.designation_id = designation.id
        d.user_id = designation.user_id
        
        d.start = self.start.data
        d.end = self.end.data
        d.end_type = self.functionEndType.data
        d.function_id = self.function.data
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        d.place_id = self.place.data
        session.add(d)

        promoteToLog = {
            'designation': {
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
        }
        log = SilegLog()
        log.type = SilegLogTypes.CREATE
        log.entity_id = d.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([promoteToLog], default=str)
        session.add(log)


class ExtendDesignationForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    start = DateTimeField('Fecha Desde', format='%d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Fecha Hasta', format='%d-%m-%Y', validators=[Optional()])

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session, silegModel.get_all_functions(session)) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [ (d.value, det2s(d)) for d in DesignationEndTypes ]
        
    def save(self, session, designation: Designation, authorizer_id):
        d = Designation()
        d.id = str(uuid.uuid4())
        d.type = DesignationTypes.EXTENSION
        d.designation_id = designation.id
        d.user_id = designation.user_id
        d.place_id = designation.place_id
        d.function_id = designation.function_id

        d.start = self.start.data
        d.end = self.end.data
        d.end_type = DesignationEndTypes(self.functionEndType.data)
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data

        session.add(d)

        extendToLog = {
            'designation': {
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
        }
        log = SilegLog()
        log.type = SilegLogTypes.CREATE
        log.entity_id = d.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([extendToLog], default=str)
        session.add(log)


class DischargeDesignationForm(FlaskForm):
    # Datos del cargo
    start = DateTimeField('Fecha Baja', format='%d-%m-%Y', validators=[DataRequired()])

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    observations = SelectField('Finaliza', coerce=str)

    def __init__(self):
        super().__init__()
        self._load_values()

    def _load_values(self):
        tipos = [
            'Fallecimiento',
            'Renuncia',
            'Término de Designación',
            'Cambio de Cátedra',
            'Termino de Extensión',
            'Limitación de Funciones',
            'Término de Licencia',
            'Cambio de Licencia',
            'reintegro de licencia',
            'Jubilación',
            'Limitacion de Cargo'
        ]
        self.observations.choices = [ (f,f) for f in tipos ]

    def save(self, session, authorizer_id , designation_to_discharge: Designation):
        designation_to_discharge.historic = True

        d = Designation()
        d.id = str(uuid.uuid4())
        d.type = DesignationTypes.DISCHARGE
        d.designation_id = designation_to_discharge.id
        d.user_id = designation_to_discharge.user_id
        d.place_id = designation_to_discharge.place_id
        d.function_id = designation_to_discharge.function_id
        d.end_type = DesignationEndTypes.INDETERMINATE
        
        d.start = self.start.data
        
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data

        d.comments = self.observations.data

        session.add(d)

        dischargeToLog = {
            'designation': {
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
        }
        log = SilegLog()
        log.type = SilegLogTypes.CREATE
        log.entity_id = d.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([dischargeToLog], default=str)
        session.add(log)


class DeleteDesignationForm(FlaskForm):

    def save(self, session, designation: Designation, authorizer_id):
        designation.deleted = datetime.datetime.now()
        designation.historic = True

        deleteToLog = {
            'designation': {
                'id': designation.id,
                'created': designation.created,
                'updated': designation.updated,
                'deleted': designation.deleted,
                'start': designation.start,
                'end': designation.end,
                'end_type': designation.end_type,
                'historic': designation.historic,
                'exp': designation.exp,
                'res': designation.res,
                'cor': designation.cor,
                'status': designation.status,
                'type': designation.type,
                'designation_id': designation.designation_id,
                'user_id': designation.user_id,
                'function_id': designation.function_id,
                'place_id': designation.place_id,
                'comments': designation.comments,
            }
        }
        log = SilegLog()
        log.type = SilegLogTypes.DELETE
        log.entity_id = designation.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([deleteToLog], default=str)
        session.add(log)


class DesignationSearchForm(FlaskForm):
    query = StringField('Buscar designaciones por nombre, apellido o número de documento')
    class Meta:
        csrf = False

class PersonSearchForm(FlaskForm):
    query = StringField('Buscar persona por apellido o número de documento')
    class Meta:
        csrf = False        


    
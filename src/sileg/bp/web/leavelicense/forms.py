import uuid
import json
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.validators import ValidationError, DataRequired, Optional

from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.LeaveLicense import PersonalLeaveLicense, DesignationLeaveLicense, LicenseTypes, LicenseEndTypes
from sileg_model.model.entities.Log import SilegLog, SilegLogTypes

def lt2s(t:LicenseTypes):
    if t == LicenseTypes.INDETERMINATE:
        return 'Indeterminado'
    if t == LicenseTypes.LICENSE:
        return 'Licencia'
    if t == LicenseTypes.DESIGNATION_RETENTION:
        return 'Retención Cargo'
    if t == LicenseTypes.SUSPENDED_PAYMENT:
        return 'Renta Suspendida'
    if t == LicenseTypes.SUSPENSION:
        return 'Suspención'
    if t == LicenseTypes.TRANSITORY_SUSPENSION:
        return 'Suspención Transitoria'
    if t == LicenseTypes.EXTENSION:
        return 'Prórroga'
    if t == LicenseTypes.DISCHARGE:
        return 'Baja'
    return ''

def et2s(t:LicenseEndTypes):
    if t == LicenseEndTypes.INDETERMINATE:
        return 'Indeterminado'
    if t == LicenseEndTypes.LICENSE_END:
        return 'Fin de licencia'
    if t == LicenseEndTypes.LICENSE_CHANGE:
        return 'Cambio de licencia'
    if t == LicenseEndTypes.DESIGNATION_END:
        return 'Fin de designación'
    if t == LicenseEndTypes.REINCORPORATION:
        return 'Reincorporación'
    return ''

class LeaveLicensePersonalCreateForm(FlaskForm):
    #Licencia
    type = SelectField('Tipo de licencia',coerce=str)
    article = SelectField('Artículo',coerce=str)
    paid = BooleanField('Goce de Sueldo')
    start = DateTimeField('Fecha Desde', format='%d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Fecha Hasta', format='%d-%m-%Y', validators=[Optional()])
    end_type = SelectField('Tipo Fin de Licencia')

    # Resolucion de Alta
    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')
    
    def __init__(self):
        super().__init__()
        self.type.choices = [ (t.value, lt2s(t)) for t in LicenseTypes ]
        self.end_type.choices = [ (t.value, et2s(t)) for t in LicenseEndTypes ]
        self.article.choices = [('0','Seleccione una opción...'),('0','CONSULTAR ARTICULOS')]

    def save(self, session, silegModel:SilegModel, uid, authorizer_id):
        l = PersonalLeaveLicense()
        l.id = str(uuid.uuid4())
        l.created = datetime.datetime.utcnow()
        l.user_id = uid
        l.type = self.type.data
        l.start = self.start.data
        l.end = self.end.data
        l.end_type = self.end_type.data
        l.cor = self.cor.data
        l.exp = self.exp.data
        l.res = self.res.data
        session.add(l)
        licenseToLog = {
            'personalLeaveLicence': {
                'id': l.id,
                'created': l.created,
                'updated': l.updated,
                'deleted': l.deleted,
                'user_id': l.user_id,
                'type': l.type,
                'start': l.start,
                'end': l.end,
                'end_type': l.end_type,
                'exp': l.exp,
                'res': l.res,
                'cor': l.cor
            }
        }
        log = SilegLog()
        log.type = SilegLogTypes.CREATE
        log.entity_id = l.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([licenseToLog], default=str)
        session.add(log)


class DesignationLeaveLicenseCreateForm(FlaskForm):
    #Licencia
    type = SelectField('Tipo de licencia',coerce=str)
    article = SelectField('Artículo',coerce=str)
    paid = BooleanField('Goce de Sueldo')
    start = DateTimeField('Fecha Desde', format='%d-%m-%Y', validators=[DataRequired()])
    end = DateTimeField('Fecha Hasta', format='%d-%m-%Y', validators=[Optional()])
    end_type = SelectField('Tipo Fin de Licencia')

    # Resolucion de Alta
    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')
    
    def __init__(self):
        super().__init__()
        self.type.choices = [ (t.value, lt2s(t)) for t in LicenseTypes ]
        self.end_type.choices = [ (t.value, et2s(t)) for t in LicenseEndTypes ]
        self.article.choices = [('0','Seleccione una opción...'),('0','CONSULTAR ARTICULOS')]

    def save(self, session, silegModel:SilegModel, did, authorizer_id):
        l = DesignationLeaveLicense()
        l.id = str(uuid.uuid4())
        l.created = datetime.datetime.utcnow()
        l.designation_id = did
        l.type = self.type.data
        l.start = self.start.data
        l.end = self.end.data
        l.end_type = self.end_type.data
        l.cor = self.cor.data
        l.exp = self.exp.data
        l.res = self.res.data
        session.add(l)

        leaveToLog = {
            'designationLeaveLicence': {
                'id': l.id,
                'created': l.created,
                'updated': l.updated,
                'deleted': l.deleted,
                'designation_id': l.designation_id,
                'type' : l.type,
                'start' : l.start,
                'end' : l.end,
                'end_type' : l.end_type,
                'cor' : l.cor,
                'exp' : l.exp,
                'res' : l.res,
            }
        }

        log = SilegLog()
        log.type = SilegLogTypes.CREATE
        log.entity_id = l.id
        log.authorizer_id = authorizer_id
        log.data = json.dumps([leaveToLog], default=str)
        session.add(log)

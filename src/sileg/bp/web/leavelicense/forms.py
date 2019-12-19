from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.validators import ValidationError, DataRequired, Optional

from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.LeaveLicense import PersonalLeaveLicense, DesignationLeaveLicense, LicenseTypes, LicenseEndTypes

def lt2s(t:LicenseTypes):
    if t == LicenseTypes.INDETERMINATE:
        return 'Indeterminado'
    if t == LicenseTypes.LIC:
        return 'Licencia'
    if t == LicenseTypes.RC:
        return 'Retención Cargo'
    if t == LicenseTypes.RS:
        return 'Renta Suspendida'
    return ''

def et2s(t:LicenseEndTypes):
    if t == LicenseEndTypes.INDETERMINATE:
        return 'Indeterminado'
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
        self.article.choices = [('0','Seleccione una opción...'),('0','Ejemplo 1'),('0','Ejemplo 2'),('0','Ejemplo 3')]

    def save(self, session, silegModel:SilegModel, uid):
        l = PersonalLeaveLicense()
        l.user_id = uid
        l.type = self.type.data
        l.start = self.start.data
        l.end = self.end.data
        l.end_type = self.end_type.data
        l.cor = self.cor.data
        l.exp = self.exp.data
        l.res = self.res.data
        session.add(l)


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
        self.article.choices = [('0','Seleccione una opción...'),('0','Ejemplo 1'),('0','Ejemplo 2'),('0','Ejemplo 3')]

    def save(self, session, silegModel:SilegModel, did):
        l = DesignationLeaveLicense()
        l.designation_id = did
        l.type = self.type.data
        l.start = self.start.data
        l.end = self.end.data
        l.end_type = self.end_type.data
        l.cor = self.cor.data
        l.exp = self.exp.data
        l.res = self.res.data
        session.add(l)


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.validators import ValidationError, DataRequired


class LeaveLicensePersonalCreateForm(FlaskForm):
    #Licencia
    leaveType = SelectField('Tipo de licencia',coerce=str)
    leaveArticle = SelectField('Artículo',coerce=str)
    paid = BooleanField('Goce de Sueldo')
    leaveFrom = DateTimeField('Fecha Desde', validators=[DataRequired()])
    leaveTo = DateTimeField('Fecha Hasta')
    leaveEndType = SelectField('Tipo Fin Cargo')
    # Resolucion de Alta
    leaveResolutionNumber = StringField('Número de resolución')
    leaveRecordNumber = StringField('Expediente')
    leaveRelatedNumber = StringField('Corresponde')
    
    def __init__(self):
        super(LeaveLicensePersonalCreateForm,self).__init__()
        self.leaveType.choices = [('0','Seleccione una opción...'),('0','Tipo de Licencia 1'),('0','Tipo de Licencia 2')]
        self.leaveArticle.choices = [('0','Seleccione una opción...'),('0','Ejemplo 1'),('0','Ejemplo 2'),('0','Ejemplo 3')]
        self.leaveEndType.choices = [('0','Seleccione una opción...'),('0','Tipo de Fin 1'),('0','Tipo de Fin 2'),('0','Tipo de Fin 3')]

class LeaveLicenseDesignationCreateForm(FlaskForm):
    #Licencia
    leaveType = SelectField('Tipo de licencia',coerce=str)
    leaveArticle = SelectField('Artículo',coerce=str)
    paid = BooleanField('Goce de Sueldo')
    leaveFrom = DateTimeField('Fecha Desde', validators=[DataRequired()])
    leaveTo = DateTimeField('Fecha Hasta')
    leaveEndType = SelectField('Tipo Fin Cargo')
    # Resolucion de Alta
    leaveResolutionNumber = StringField('Número de resolución')
    leaveRecordNumber = StringField('Expediente')
    leaveRelatedNumber = StringField('Corresponde')
    
    def __init__(self):
        super(LeaveLicenseDesignationCreateForm,self).__init__()
        self.leaveType.choices = [('0','Seleccione una opción...'),('0','Tipo de Licencia 1'),('0','Tipo de Licencia 2')]
        self.leaveArticle.choices = [('0','Seleccione una opción...'),('0','Ejemplo 1'),('0','Ejemplo 2'),('0','Ejemplo 3')]
        self.leaveEndType.choices = [('0','Seleccione una opción...'),('0','Tipo de Fin 1'),('0','Tipo de Fin 2'),('0','Tipo de Fin 3')]


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo

class ExtendDesignationForm(FlaskForm):
    newDedication = SelectField('Nueva Dedicación', coerce=str)
    dedicationFrom = DateTimeField('Fecha Desde', validators=[DataRequired()])
    dedicationTo = DateTimeField('Fecha Hasta', validators=[DataRequired()])
    resolutionNumber = StringField('Número de resolución')
    recordNumber = StringField('Expediente')
    relatedNumber = StringField('Corresponde')
    positionEndType = SelectField('Tipo Fin Cargo',coerce=str)
    
    department = SelectField('Departamento')
    departmentArea = SelectField('Materia',coerce=str)
    chair = SelectField('Cátedra',coerce=str)
    commission = StringField('Comisión')
    workArea = SelectField('Area',coerce=str)
    workPlace = SelectField('Lugar de Trabajo',coerce=str)
    function = SelectField('Función',coerce=str)
    
    dischargeType = SelectField('Tipo de baja', coerce=str) 
    dischargeDate = DateTimeField('Fecha de baja', validators=[DataRequired()])

    dischargeResolution = StringField('Número de resolución')
    dischargeRecordNumber = StringField('Expediente')
    dischargeRelatedNumber = StringField('Corresponde')

    def __init__(self):
        super(ExtendDesignationForm,self).__init__()
        self.newDedication.choices = [('0','Seleccione una opción...'),('0','A-H'),('0','Exclusiva'),('0','Semidedicacion'),('0','Semiexclusiva'),('0','Simple'),('0','Tiempo Completo')]
        self.positionEndType.choices = [('0','Seleccione una opción...'),('0','Hasta Concurso...'),('0','Hasta Convalid. Consejo Superior'),('0','Hasta nuevo llamado')]
        self.department.choices = [('0','Seleccione una opción...')]
        self.departmentArea.choices = [('0','Seleccione una opción...')]
        self.chair.choices = [('0','Seleccione una opción...')]
        self.commission.choices = [('0','Seleccione una opción...')]
        self.workArea.choices = [('0','Seleccione una opción...')]
        self.workPlace.choices = [('0','Seleccione una opción...')]
        self.function.choices = [('0','Seleccione una opción...')]        
        self.dischargeType.choices = [('0','Seleccione una opción...'),('0','Cambio de Cátedra'),('0','Cambio de Licencia'),('0','Fallecimiento'),('0','Jubilación'),('0','Limitación de Cargo'),('0','Limitación de Funciones'),('0','Reintegro de Licencia'),('0','Renuncia'),('0','Término de Designación'),('0','Término de Extensión'),('0','Término de Licencia')]

class RenewForm(FlaskForm):
    acquisitionDate = DateTimeField('Fecha de Obtención', validators=[DataRequired()])
    dedicationFrom = DateTimeField('Fecha Desde', validators=[DataRequired()])
    dedicationTo = DateTimeField('Fecha Hasta', validators=[DataRequired()])
    resolutionNumber = StringField('Número de resolución')
    recordNumber = StringField('Expediente')
    relatedNumber = StringField('Corresponde')
    positionEndType = SelectField('Tipo Fin Cargo',coerce=str)
    
    dischargeType = SelectField('Tipo de baja', coerce=str) 
    dischargeDate = DateTimeField('Fecha de baja', validators=[DataRequired()])

    dischargeResolution = StringField('Número de resolución')
    dischargeRecordNumber = StringField('Expediente')
    dischargeRelatedNumber = StringField('Corresponde')

    def __init__(self):
        super(RenewForm,self).__init__()
        self.positionEndType.choices = [('0','Seleccione una opción...'),('0','Hasta Concurso...'),('0','Hasta Convalid. Consejo Superior'),('0','Hasta nuevo llamado')]
        self.dischargeType.choices = [('0','Seleccione una opción...'),('0','Cambio de Cátedra'),('0','Cambio de Licencia'),('0','Fallecimiento'),('0','Jubilación'),('0','Limitación de Cargo'),('0','Limitación de Funciones'),('0','Reintegro de Licencia'),('0','Renuncia'),('0','Término de Designación'),('0','Término de Extensión'),('0','Término de Licencia')]

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
        self.newDedication.choices = [('0','Seleccione una opción...')]
        self.positionEndType.choices = [('0','Seleccione una opción...')]
        self.department.choices = [('0','Seleccione una opción...')]
        self.departmentArea.choices = [('0','Seleccione una opción...')]
        self.chair.choices = [('0','Seleccione una opción...')]
        self.commission.choices = [('0','Seleccione una opción...')]
        self.workArea.choices = [('0','Seleccione una opción...')]
        self.workPlace.choices = [('0','Seleccione una opción...')]
        self.function.choices = [('0','Seleccione una opción...')]        
        self.dischargeType.choices = [('0','Seleccione una opción...')]

    def validate_person_number(self, person_number):
        #if UsersModel.getUser(person_number.data):
        #    raise ValidationError('Atencion existente un usuario con ese DNI')
        pass

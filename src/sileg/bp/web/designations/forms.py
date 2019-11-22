from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo

class ExtendDesignationForm(FlaskForm):
    lastname = StringField('Apellidos', validators=[DataRequired()])
    firstname = StringField('Nombres', validators=[DataRequired()])
    person_number_type = SelectField('Tipo de Documento', coerce=str)
    person_number = StringField('Nro. de Documento', validators=[DataRequired()])
    gender = SelectField('Genero', coerce=str)
    birthplace = StringField('Ciudad de Nacimiento',validators=[DataRequired()])
    birthdate = DateTimeField('Fecha de Nacimiento',validators=[DataRequired()],format='%d-%m-%Y')
    
    residence = StringField('Ciudad de Residencia',validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    
    land_line = StringField('Telefono Fijo', validators=[])
    mobile_number =StringField('Telefono Movil', validators=[])

    ingress_date = DateTimeField('Fecha de ingreo a la FCE')
    laboral_number = StringField('CUIL')
    marital_status = SelectField('Estado Civil', coerce=str)
    retirement_date = DateTimeField('Fecha de Jubilación')
    
    
        
    def __init__(self):
        super(ExtendDesignationForm,self).__init__()
        self.person_number_type.choices = [('0','Seleccione una opción...'),('0','LC'),('0','LE'),('0','DNI'),('0','PASAPORTE')]
        self.gender.choices = [('0','Seleccione una opción...'),('0','Femenino'),('0','Masculino'),('0','Otro')]
        self.marital_status.choices = [('0','Seleccione una opción...'),('0','Casado/a'),('0','Soltero/a'),('0','Conviviente'),('0','Divorciado/a'),]

    def validate_person_number(self, person_number):
        #if UsersModel.getUser(person_number.data):
        #    raise ValidationError('Atencion existente un usuario con ese DNI')
        pass

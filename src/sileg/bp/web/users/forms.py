from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email

class UserCreateForm(FlaskForm):
    dni = StringField('DNI', validators=[DataRequired()])
    lastname = StringField('Apellido', validators=[DataRequired()])
    firstname = StringField('Nombre', validators=[DataRequired()])
    legajo = StringField('Legajo', validators=[])
    birthdate = DateTimeField('Fecha de Nacimiento',validators=[DataRequired()],format='%d-%m-%Y')
    gender = SelectField('Genero', coerce=str)
    marital_status = SelectField('Estado Civil', coerce=str)
    address = StringField('Dirección', validators=[DataRequired()])
    city = StringField('Ciudad', validators=[])
    country = StringField('Pais', validators=[])
    personal_email = EmailField('Correo Personal', validators=[DataRequired(), Email(message='Formato de correo erroneo.')])
    land_line = StringField('Telefono Fijo', validators=[])
    mobile_number =StringField('Telefono Movil', validators=[])
        
    def __init__(self):
        super(UserCreateForm,self).__init__()
        #genders = UserModel.getGenders()
        #self.gender.choices = genders if genders else [('0','Sin Opciones')]
        #marital_statuses = UserModel.getMaritalStatuses()
        #self.marital_status.choices = genders if genders else [('0','Sin Opciones')]
        self.gender.choices = [('0','Sin Opciones')]
        self.marital_status.choices = [('0','Sin Opciones')]

    def validate_dni(self, dni):
        #if UsersModel.getUser(dni.data):
        #    raise ValidationError('Atencion existente un usuario con ese DNI')
        pass

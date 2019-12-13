from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, SelectField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email

from sileg.helpers.apiHandler import getStates

from sileg.models import usersModel, open_users_session

class PersonCreateForm(FlaskForm):
    lastname = StringField('Apellidos', validators=[DataRequired()])
    firstname = StringField('Nombres', validators=[DataRequired()])
    person_number_type = SelectField('Tipo de Documento', coerce=str)
    person_number = StringField('Nro. de Documento', validators=[DataRequired()])
    gender = SelectField('Genero', coerce=str)
    marital_status = SelectField('Estado Civil', coerce=str)
    birthplace = StringField('Ciudad de Nacimiento')
    birthdate = StringField('Fecha de Nacimiento')
    residence = StringField('Ciudad de Residencia')
    address = StringField('Dirección')
    work_email = EmailField('Correo de Trabajo')
    personal_email = EmailField('Correo Personal')
    land_line = StringField('Telefono Fijo')
    mobile_number =StringField('Telefono Movil')
    person_numberFile = FileField('Adjuntar DNI')
    laboral_numberFile = FileField('Adjuntar CUIL')
    seniority_external_years = StringField('Años')
    seniority_external_months = StringField('Meses')
    seniority_external_days = StringField('Días')
        
    def __init__(self):
        super(PersonCreateForm,self).__init__()
        self.person_number_type.choices = [('0','Seleccione una opción...'),('1','LC'),('2','LE'),('3','DNI'),('4','PASAPORTE')]
        self.gender.choices = [('0','Seleccione una opción...'),('1','Femenino'),('2','Masculino'),('3','Autopercibido')]
        self.marital_status.choices = [('0','Seleccione una opción...'),('1','Casado/a'),('2','Soltero/a'),('3','Conviviente'),('4','Divorciado/a'),]

    def validate_person_number_type(self, person_number_type):
        if self.person_number_type.data == '0':
            raise ValidationError('Debe seleccionar una opción')   

    def validate_seniority_external_years(self,seniority_external_years):
        if self.seniority_external_years.data:
            try:
                number = int(self.seniority_external_years.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor a 0')
    
    def validate_seniority_external_months(self,seniority_external_months):
        if self.seniority_external_months.data:
            try:
                number = int(self.seniority_external_months.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor a 0')
    
    def validate_seniority_external_days(self,seniority_external_days):
        if self.seniority_external_days.data:
            try:
                number = int(self.seniority_external_days.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor a 0')

    def save(self):
        """
        Persistencia de datos en DB
        """
        data = {
        'lastname' : self.lastname.data,
        'firstname' : self.firstname.data,
        'person_number_type' : self.person_number_type.data,
        'person_number' : self.person_number.data,
        'gender' : self.gender.data,
        'marital_status' : self.marital_status.data,
        'birthplace' : self.birthplace.data,
        'birthdate' : self.birthdate.data,
        'residence' : self.residence.data,
        'address' : self.address.data,
        'work_email' : self.work_email.data,
        'personal_email' : self.personal_email.data,
        'land_line' : self.land_line.data,
        'mobile_number' : self.mobile_number.data,
        'person_numberFile' : self.person_numberFile.data,
        'laboral_numberFile' : self.laboral_numberFile.data,
        'seniority_external_years' : self.seniority_external_years.data,
        'seniority_external_months'  : self.seniority_external_months.data,
        'seniority_external_days' : self.seniority_external_days.data
        }
        print(data)

class TitleAssignForm(FlaskForm):
    titleType = SelectField('Tipo de Título')
    titleDate = StringField('Fecha de Obtención')
    titleName = SelectField('Nombre del Título')
    titleFile = FileField('Adjuntar Título')
        
    def __init__(self):
        super(TitleAssignForm,self).__init__()
        #TODO Obtener del modelo los titulos existentes y tipos
        self.titleType.choices = [('0','Seleccione una opción...'),('1','Grado'),('2','Posgrado')]
        self.titleName.choices = [('0','Seleccione una opción...'),('1','Contador'),('2','Ingeniero'),('3','Licenciado en Ciencias Administrativas')]

    def validate_titleType(self, titleType):
        if self.titleType.data == '0':
            raise ValidationError('Debe seleccionar una opción')
    def validate_titleName(self, titleName):
        if self.titleName.data == '0':
            raise ValidationError('Debe seleccionar una opción')

class PersonSearchForm(FlaskForm):
    query = StringField('Buscar persona por apellido o número de documento')
    class Meta:
        csrf = False
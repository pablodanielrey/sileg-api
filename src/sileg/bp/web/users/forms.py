from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email

from sileg.helpers.apiHandler import getStates

class UserCreateForm(FlaskForm):
    lastname = StringField('Apellidos', validators=[DataRequired()])
    firstname = StringField('Nombres', validators=[DataRequired()])
    person_number_type = SelectField('Tipo de Documento', coerce=str)
    person_number = StringField('Nro. de Documento', validators=[DataRequired()])
    gender = SelectField('Genero', coerce=str)
    birthplace_state = SelectField('Provincia de Nacimiento',coerce=str)
    birthplace_city = SelectField('Ciudad de Nacimiento',coerce=str)
    birthdate = DateTimeField('Fecha de Nacimiento',validators=[DataRequired()],format='%d-%m-%Y')
    
    residence_state = SelectField('Provincia de Residencia',coerce=str)
    residence_city = SelectField('Ciudad de Recidencia',coerce=str)
    address = StringField('Dirección', validators=[DataRequired()])
    
    work_email = EmailField('Correo de Trabajo', validators=[DataRequired(), Email(message='Formato de correo erroneo.')])
    personal_email = EmailField('Correo Personal', validators=[DataRequired(), Email(message='Formato de correo erroneo.')])
    
    land_line = StringField('Telefono Fijo', validators=[])
    mobile_number =StringField('Telefono Movil', validators=[])

    #seniority_to_date = DateTimeField('Antigüedad al Día')
    #seniority_rented_internal = DateTimeField('Antigüedad Rentada Interna')
    #seniority_rented_external = DateTimeField('Antigüedad Rentada Externa')
    #seniority_rented_total = DateTimeField('Antigüedad Rentada Total')
    #seniority_rented_unused = DateTimeField('Antigüedad Rentada No Utilizada')
    #seniority_ad_honorem = DateTimeField('Antigüedad Ad-Honorem')
    #seniority_rented_exported = DateTimeField('Antigüedad Rentada Exportada')
    #seniority_ad_honorem = BooleanField('¿Antigüedad Ad-Honorem Computable?	')
    #seniority_observations = StringField('Observaciones')

    ingress_date = DateTimeField('Fecha de ingreo a la FCE')
    laboral_number = StringField('CUIL')
    marital_status = SelectField('Estado Civil', coerce=str)
    #prepaid_medicine = SelectField('Obra Social', coerce=str)
    #life_insurance = SelectField('Seguro de Vida', coerce=str)
    #life_insurance_account = StringField('Cuenta Nro.')
    #bank_branch = SelectField('Cobra en Banco/Sucursal', coerce=str)
    retirement_date = DateTimeField('Fecha de Jubilación')

    #life_insurance_mandatary = BooleanField('Obligatorio')
    #life_insurance_bank = SelectField('Banco', coerce=str)
    #life_insurance_policy_number1 = StringField('Poliza Número 1')
    #life_insurance_policy_number2 = StringField('Poliza Número 2')
    #life_insurance_policy_number3 = StringField('Poliza Número 3')
       
        
    def __init__(self):
        super(UserCreateForm,self).__init__()
        self.person_number_type.choices = [('0','Sin Opciones')]
        self.gender.choices = [('0','Sin Opciones')]
        self.marital_status.choices = [('0','Sin Opciones')]
        self.birthplace_state.choices = getStates()
        self.birthplace_city.choices = [('0','Sin Opciones')]
        self.residence_state.choices = getStates()
        self.residence_city.choices = [('0','Sin Opciones')]
        self.marital_status.choices = [('0','Sin Opciones')]
        #self.prepaid_medicine.choices = [('0','Sin Opciones')]
        #self.life_insurance.choices = [('0','Sin Opciones')]
        #self.bank_branch.choices = [('0','Sin Opciones')]

    def validate_person_number(self, person_number):
        #if UsersModel.getUser(person_number.data):
        #    raise ValidationError('Atencion existente un usuario con ese DNI')
        pass


class UserSearchForm(FlaskForm):
    query = StringField('Buscar usuarios por apellido o número de documento')
    class Meta:
        csrf = False
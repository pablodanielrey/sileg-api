import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, SelectField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email

from sileg.helpers.apiHandler import getStates

from sileg.models import usersModel, open_users_session
from users.model.entities.User import User, Mail, Phone, UserFiles, MailTypes, PhoneTypes, UserFileTypes, UsersLog, UserLogTypes

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
    personal_email = EmailField('Correo Personal',validators=[DataRequired()])
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

    def save(self,authorizer_id):
        """
        Persistencia de datos en DB
        """
        toLog = []
        with open_users_session() as session:
            if not usersModel.get_uid_person_number(session, self.person_number.data):
                newUser = User()
                newUser.lastname = self.lastname.data
                newUser.firstname = self.firstname.data
                newUser.person_number_type = self.person_number_type.data
                newUser.person_number = self.person_number.data
                newUser.gender = self.gender.data if self.gender.data != '0' else None
                newUser.marital_status = self.marital_status.data if self.marital_status.data != '0' else None
                newUser.birthplace = self.birthplace.data
                newUser.birthdate = self.birthdate.data if self.birthdate.data else None
                newUser.residence = self.residence.data
                newUser.address = self.address.data
                session.add(newUser)
                toLog.append(newUser.as_dict())
                
                if self.work_email.data:
                    newWorkEmail = Mail()
                    newWorkEmail.email = self.work_email.data
                    newWorkEmail.type = MailTypes.INSTITUTIONAL
                    newWorkEmail.user_id = newUser.id
                    session.add(newWorkEmail)
                    toLog.append({  'id': newWorkEmail.id,
                                    'created': newWorkEmail.created,
                                    'updated': newWorkEmail.updated,
                                    'deleted': newWorkEmail.deleted,
                                    'type': newWorkEmail.type.value,
                                    'email': newWorkEmail.email,
                                    'confirmed': newWorkEmail.confirmed,
                                    'user_id': newWorkEmail.user_id,
                                })

                if self.personal_email.data:
                    newPersonalMail = Mail()
                    newPersonalMail.email = self.personal_email.data
                    newPersonalMail.type = MailTypes.NOTIFICATION
                    newPersonalMail.user_id = newUser.id
                    session.add(newPersonalMail)
                    toLog.append({  'id': newPersonalMail.id,
                                    'created': newPersonalMail.created,
                                    'updated': newPersonalMail.updated,
                                    'deleted': newPersonalMail.deleted,
                                    'type': newPersonalMail.type.value,
                                    'email': newPersonalMail.email,
                                    'confirmed': newPersonalMail.confirmed,
                                    'user_id': newPersonalMail.user_id,
                                })

                if self.land_line.data:
                    landLinePhone = Phone()
                    landLinePhone.type = PhoneTypes.LANDLINE
                    landLinePhone.number = self.land_line.data
                    landLinePhone.user_id = newUser.id
                    session.add(landLinePhone)
                    toLog.append({  'id': landLinePhone.id,
                                    'created': landLinePhone.created,
                                    'updated': landLinePhone.updated,
                                    'deleted': landLinePhone.deleted,
                                    'type': landLinePhone.type.value,
                                    'email': landLinePhone.email,
                                    'confirmed': landLinePhone.confirmed,
                                    'user_id': landLinePhone.user_id,
                                })

                if self.mobile_number.data:
                    mobileNumber = Phone()
                    mobileNumber.type = PhoneTypes.CELLPHONE
                    mobileNumber.number = self.mobile_number.data
                    mobileNumber.user_id = newUser.id
                    session.add(mobileNumber)
                    toLog.append({  'id': mobileNumber.id,
                                    'created': mobileNumber.created,
                                    'updated': mobileNumber.updated,
                                    'deleted': mobileNumber.deleted,
                                    'type': mobileNumber.type.value,
                                    'email': mobileNumber.email,
                                    'confirmed': mobileNumber.confirmed,
                                    'user_id': mobileNumber.user_id,
                                })

                if self.person_numberFile.data:
                    personNumberFile = UserFiles()
                    personNumberFile.mimetype = None
                    personNumberFile.type = UserFileTypes.PERSONNUMBER
                    personNumberFile.content = None
                    session.add(personNumberFile)
                    toLog.append(personNumberFile.as_dict())

                if self.laboral_numberFile.data:
                    laboralNumberFile = UserFiles()
                    laboralNumberFile.mimetype = None
                    laboralNumberFile.type = UserFileTypes.LABORALNUMBER
                    laboralNumberFile.content = None
                    session.add(laboralNumberFile)
                    toLog.append(laboralNumberFile.as_dict())

                newLog = UsersLog()
                newLog.entity_id = newUser.id
                newLog.authorizer_id = authorizer_id
                newLog.type = UserLogTypes.CREATE
                newLog.data = json.dumps(toLog)
                session.add(newLog)
                session.commit()

        #TODO Sileg model
        newSeniority = {
            'seniority_external_years' : self.seniority_external_years.data,
            'seniority_external_months'  : self.seniority_external_months.data,
            'seniority_external_days' : self.seniority_external_days.data
        }
        #TODO Guardar datos modificados en tabla separada JSON

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
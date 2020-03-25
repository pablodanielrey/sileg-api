import json
import uuid
import base64
import datetime
import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, SelectField, SubmitField
from flask_wtf.file import FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email, InputRequired

from sileg.helpers.apiHandler import getStates
from sileg.helpers.namesHandler import id2sDegrees, id2sIdentityNumber

from sileg.models import usersModel, open_users_session, silegModel, open_sileg_session
from users.model.entities.User import User, IdentityNumber, Mail, Phone, File, MailTypes, PhoneTypes, UsersLog, UserLogTypes, IdentityNumberTypes, DegreeTypes, UserDegree

from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.ExternalSeniority import ExternalSeniority
from sileg_model.model.entities.Log import SilegLog, SilegLogTypes

class ResetCredentialsForm(FlaskForm):
    modifyCredentials = SubmitField('Blanquear Clave')
    
    
class PersonCreateForm(FlaskForm):
    """

    MODELO DE USUARIOS
    
    """
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
    person_numberFile = FileField('Adjuntar Documento')
    laboral_number = StringField('CUIL')
    laboral_numberFile = FileField('Adjuntar CUIL')
    seniority_external_years = StringField('Años')
    seniority_external_months = StringField('Meses')
    seniority_external_days = StringField('Días')
        
    def __init__(self):
        super(PersonCreateForm,self).__init__()
        self.person_number_type.choices = [('0','Seleccione una opción...'),('DNI','DNI'),('LC','LC'),('LE','LE'),('PASSPORT','Pasaporte')]
        self.gender.choices = [('0','Seleccione una opción...'),('Femenino','Femenino'),('Masculino','Masculino'),('Autopercibido','Autopercibido')]
        self.marital_status.choices = [('0','Seleccione una opción...'),('Casado/a','Casado/a'),('Soltero/a','Soltero/a'),('Conviviente','Conviviente'),('Divorciado/a','Divorciado/a'),('Viudo/a','Viudo/a')]

    def validate_person_number_type(self, person_number_type):
        if self.person_number_type.data == '0':
            raise ValidationError('Debe seleccionar una opción')   

    def validate_personal_email(self, personal_email):
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]*econo.unlp.edu.ar$",self.personal_email.data) != None:
            raise ValidationError('El correo electrónico personal no puede ser institucional')

    def validate_seniority_external_years(self,seniority_external_years):
        if self.seniority_external_years.data:
            try:
                number = int(self.seniority_external_years.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor o igual 0')
    
    def validate_seniority_external_months(self,seniority_external_months):
        if self.seniority_external_months.data:
            try:
                number = int(self.seniority_external_months.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor o igual a 0')
            if number > 11:
                raise ValidationError('Utilice un número entre 0 y 11')
    
    def validate_seniority_external_days(self,seniority_external_days):
        if self.seniority_external_days.data:
            try:
                number = int(self.seniority_external_days.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor o igual a 0')
            if number > 29:
                raise ValidationError('Utilice un número entre 0 y 29')

    def save(self,authorizer_id):
        """
        Persistencia de datos en DB
        """
        toLog = {}
        uid = str(uuid.uuid4())
        with open_users_session() as users_session:
            if not usersModel.get_uid_person_number(users_session, self.person_number.data):
                newUser = User()
                newUser.id = uid
                newUser.created = datetime.datetime.utcnow()
                newUser.lastname = self.lastname.data
                newUser.firstname = self.firstname.data
                newUser.gender = self.gender.data if self.gender.data != '0' else None
                newUser.marital_status = self.marital_status.data if self.marital_status.data != '0' else None
                newUser.birthplace = self.birthplace.data
                newUser.birthdate = self.birthdate.data if self.birthdate.data else None
                newUser.residence = self.residence.data
                newUser.address = self.address.data
                users_session.add(newUser)
                toLog['user'] = {
                        'id': newUser.id,
                        'created': newUser.created,
                        'updated': newUser.updated,
                        'deleted': newUser.deleted,
                        'lastname': newUser.lastname,
                        'firstname': newUser.firstname,
                        'gender': newUser.gender,
                        'marital_status': newUser.marital_status,
                        'birthplace': newUser.birthplace,
                        'birthdate': newUser.birthdate,
                        'residence': newUser.residence,
                        'address': newUser.address,
                }

                """ Se carga archivo documento """
                person_file_id = None
                if self.person_numberFile.data:
                    person_file_id = str(uuid.uuid4())                    
                    personNumberFile = File()
                    personNumberFile.id = person_file_id
                    personNumberFile.created = datetime.datetime.utcnow()
                    personNumberFile.mimetype = self.person_numberFile.data.mimetype
                    personNumberFile.content = base64.b64encode(self.person_numberFile.data.read()).decode()
                    users_session.add(personNumberFile)
                    toLog['IdentityNumberFile'] = {
                            'id': personNumberFile.id,
                            'created': personNumberFile.created,
                            'updated': personNumberFile.updated,
                            'deleted': personNumberFile.deleted,
                            'mimetype': personNumberFile.mimetype,
                            'content': personNumberFile.content,
                    }

                """ Se genera documento """
                idNumber = IdentityNumber()
                idNumber.id = str(uuid.uuid4())
                idNumber.created = datetime.datetime.utcnow()
                idNumber.type = self.person_number_type.data
                idNumber.number = self.person_number.data
                idNumber.user_id = uid
                if person_file_id:
                    idNumber.file_id = person_file_id
                users_session.add(idNumber)
                toLog['identity_number'] = {
                        'id': idNumber.id,
                        'created': idNumber.created,
                        'updated': idNumber.updated,
                        'deleted': idNumber.deleted,
                        'type': idNumber.type,
                        'number': idNumber.number,
                        'user_id': idNumber.user_id,
                }

                """ Se genera correo laboral """
                if self.work_email.data:
                    newWorkEmail = Mail()
                    newWorkEmail.id = str(uuid.uuid4())
                    newWorkEmail.created = datetime.datetime.utcnow()
                    emailType = MailTypes.NOTIFICATION
                    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]*econo.unlp.edu.ar$",self.work_email.data) != None:
                        emailType = MailTypes.INSTITUTIONAL
                    newWorkEmail.type = emailType
                    newWorkEmail.email = self.work_email.data
                    newWorkEmail.user_id = uid
                    users_session.add(newWorkEmail)
                    toLog['workMail'] = {
                            'id': newWorkEmail.id,
                            'created': newWorkEmail.created,
                            'updated': newWorkEmail.updated,
                            'deleted': newWorkEmail.deleted,
                            'type': newWorkEmail.type.value,
                            'email': newWorkEmail.email,
                            'confirmed': newWorkEmail.confirmed,
                            'user_id': newWorkEmail.user_id,
                    }

                """ Se genera correo personal """
                if self.personal_email.data:
                    newPersonalMail = Mail()
                    newPersonalMail.id = str(uuid.uuid4())
                    newPersonalMail.created = datetime.datetime.utcnow()
                    newPersonalMail.type = MailTypes.ALTERNATIVE
                    newPersonalMail.email = self.personal_email.data
                    newPersonalMail.user_id = uid
                    newPersonalMail.confirmed = datetime.datetime.utcnow()
                    users_session.add(newPersonalMail)
                    toLog['personMail'] = {
                            'id': newPersonalMail.id,
                            'created': newPersonalMail.created,
                            'updated': newPersonalMail.updated,
                            'deleted': newPersonalMail.deleted,
                            'type': newPersonalMail.type.value,
                            'email': newPersonalMail.email,
                            'confirmed': newPersonalMail.confirmed,
                            'user_id': newPersonalMail.user_id,
                    }

                """ Se genera telefono fijo """
                if self.land_line.data:
                    landLinePhone = Phone()
                    landLinePhone.id = str(uuid.uuid4())
                    landLinePhone.created = datetime.datetime.utcnow()
                    landLinePhone.type = PhoneTypes.LANDLINE
                    landLinePhone.number = self.land_line.data
                    landLinePhone.user_id = uid
                    users_session.add(landLinePhone)
                    toLog['landlinePhone'] = {
                            'id': landLinePhone.id,
                            'created': landLinePhone.created,
                            'updated': landLinePhone.updated,
                            'deleted': landLinePhone.deleted,
                            'type': landLinePhone.type.value,
                            'number': landLinePhone.number,
                            'user_id': landLinePhone.user_id,
                    }

                """ Se genera telefono movil """
                if self.mobile_number.data:
                    mobileNumber = Phone()
                    mobileNumber.id = str(uuid.uuid4())
                    mobileNumber.created = datetime.datetime.utcnow()
                    mobileNumber.type = PhoneTypes.CELLPHONE
                    mobileNumber.number = self.mobile_number.data
                    mobileNumber.user_id = uid
                    users_session.add(mobileNumber)
                    toLog['mobilePhone'] = {
                            'id': mobileNumber.id,
                            'created': mobileNumber.created,
                            'updated': mobileNumber.updated,
                            'deleted': mobileNumber.deleted,
                            'type': mobileNumber.type.value,
                            'number': mobileNumber.number,
                            'user_id': mobileNumber.user_id,
                    }

                if self.laboral_number.data:
                    cid = str(uuid.uuid4())
                    cuil = IdentityNumber()
                    cuil.id = cid
                    cuil.created = datetime.datetime.utcnow()
                    cuil.type = IdentityNumberTypes.CUIL
                    cuil.number = self.laboral_number.data
                    cuil.user_id = uid

                    """ Se genera archivo de cuil """
                    cfid = None
                    if self.laboral_numberFile.data:
                        cfid = str(uuid.uuid4())
                        laboralNumberFile = File()
                        laboralNumberFile.id = cfid
                        laboralNumberFile.created = datetime.datetime.utcnow()
                        laboralNumberFile.mimetype = self.laboral_numberFile.data.mimetype
                        laboralNumberFile.content = base64.b64encode(self.laboral_numberFile.data.read()).decode()
                        users_session.add(laboralNumberFile)
                        toLog['laboralNumberFile'] = {
                                'id': laboralNumberFile.id,
                                'created': laboralNumberFile.created,
                                'updated': laboralNumberFile.updated,
                                'deleted': laboralNumberFile.deleted,
                                'mimetype': laboralNumberFile.mimetype,
                                'content': laboralNumberFile.content,
                                'identityNumber': cid,
                        }
                    if cfid:
                        cuil.file_id = cfid
                    users_session.add(cuil)
                    toLog['laboralNumber'] = {
                            'id': cuil.id,
                            'created': cuil.created,
                            'updated': cuil.updated,
                            'deleted': cuil.deleted,
                            'type': cuil.type,
                            'number': cuil.number,
                            'user_id': cuil.user_id,
                    }

                newLog = UsersLog()
                newLog.entity_id = newUser.id
                newLog.authorizer_id = authorizer_id
                newLog.type = UserLogTypes.CREATE
                newLog.data = json.dumps([toLog], default=str)
                users_session.add(newLog)
                
                with open_sileg_session() as sileg_session:
                    if (self.seniority_external_years.data or self.seniority_external_months.data or self.seniority_external_days.data) and (self.seniority_external_years.data != '0' or self.seniority_external_months.data != '0' or self.seniority_external_days.data != '0'):
                        newSeniority = {
                            'seniority_external_years' : int(self.seniority_external_years.data) if self.seniority_external_years.data else 0,
                            'seniority_external_months'  : int(self.seniority_external_months.data) if self.seniority_external_months.data else 0,
                            'seniority_external_days' : int(self.seniority_external_days.data) if self.seniority_external_days.data else 0
                        }
                        external_seniority = ExternalSeniority()
                        external_seniority.id = str(uuid.uuid4())
                        external_seniority.created = datetime.datetime.utcnow()
                        external_seniority.user_id = uid
                        external_seniority.years = newSeniority['seniority_external_years']
                        external_seniority.months = newSeniority['seniority_external_months']
                        external_seniority.days = newSeniority['seniority_external_days']
                        sileg_session.add(external_seniority)
                        external_seniority_log = {  
                            'external_seniority' : {
                                'id': external_seniority.id,
                                'created': external_seniority.created,
                                'updated': external_seniority.updated,
                                'deleted': external_seniority.deleted,
                                'days': external_seniority.days,
                                'months': external_seniority.months,
                                'years': external_seniority.years,
                                'user_id': external_seniority.user_id
                            }
                        }
                        log = SilegLog()
                        log.type = SilegLogTypes.CREATE
                        log.entity_id = external_seniority.id
                        log.authorizer_id = authorizer_id
                        log.data = json.dumps([external_seniority_log], default=str)
                        sileg_session.add(log)
                        try:
                            sileg_session.commit()
                            users_session.commit()
                        except:
                            return None
                    else:
                        users_session.commit()
                return self.person_number.data
            else:
                return None

        
class DegreeAssignForm(FlaskForm):
    degreeType = SelectField('Tipo de Título')
    degreeDate = DateTimeField('Fecha de Obtención',format='%d-%m-%Y')
    degreeName = StringField('Nombre del Título',validators=[DataRequired(message='Debe especificar nombre de título.')])
    degreeFile = FileField('Adjuntar Título')
        
    def __init__(self):
        super(DegreeAssignForm,self).__init__()
        #TODO Obtener del modelo los titulos existentes y tipos
        degreeChoices = [(id.value, id2sDegrees(id)) for id in DegreeTypes]
        degreeChoices.insert(0,('0','Seleccione...'))
        self.degreeType.choices = degreeChoices

    def validate_degreeType(self, degreeType):
        if self.degreeType.data == '0':
            raise ValidationError('Debe seleccionar una opción')

    def save(self,uid,authorizer_id):
        """ Persiste datos del formulario en la base """
        toLog = {}
        with open_users_session() as session:
            if usersModel.get_users(session, [uid])[0]:
                """ Se carga archivo del titulo si existe """
                degree_file_id = None
                if self.degreeFile.data:
                    degree_file_id = str(uuid.uuid4())                    
                    degreeFile = File()
                    degreeFile.id = degree_file_id
                    degreeFile.created = datetime.datetime.utcnow()
                    degreeFile.mimetype = self.degreeFile.data.mimetype
                    degreeFile.content = base64.b64encode(self.degreeFile.data.read()).decode()
                    session.add(degreeFile)
                    toLog['file'] = {
                            'id': degreeFile.id,
                            'created': degreeFile.created,
                            'updated': degreeFile.updated,
                            'deleted': degreeFile.deleted,
                            'mimetype': degreeFile.mimetype,
                            'content': degreeFile.content,
                    }
                    
                did = str(uuid.uuid4())
                newDegree = UserDegree()
                newDegree.id = did
                newDegree.created = datetime.datetime.utcnow()
                newDegree.type = self.degreeType.data
                newDegree.title = self.degreeName.data
                newDegree.start = self.degreeDate.data if self.degreeDate.data else None
                newDegree.user_id = uid
                if degree_file_id:
                    newDegree.file_id = degree_file_id
                session.add(newDegree)
                toLog['user_degree'] = {
                        'id': newDegree.id,
                        'created': newDegree.created,
                        'updated': newDegree.updated,
                        'deleted': newDegree.deleted,
                        'title': newDegree.title,
                        'start': newDegree.start,
                        'user_id': newDegree.user_id,
                    }

                newLog = UsersLog()
                newLog.entity_id = did
                newLog.authorizer_id = authorizer_id
                newLog.type = UserLogTypes.CREATE
                newLog.data = json.dumps([toLog], default=str)
                session.add(newLog)
                session.commit()

class PersonSearchForm(FlaskForm):
    query = StringField('Buscar persona por apellido o número de documento')
    class Meta:
        csrf = False

class PersonDataModifyForm(FlaskForm):
    lastname = StringField('Apellidos', validators=[InputRequired()])
    firstname = StringField('Nombres', validators=[InputRequired()])
    gender = SelectField('Género', coerce=str)
    marital_status = SelectField('Estado Civil', coerce=str)
    birthplace = StringField('Ciudad de Nacimiento')
    birthdate = StringField('Fecha de Nacimiento')
    residence = StringField('Ciudad de Residencia')
    address = StringField('Dirección')
    personDataModify = SubmitField('Guardar Cambios')
        
    def __init__(self):
        super(PersonDataModifyForm,self).__init__()
        self.gender.choices = [('0','Seleccione una opción...'),('Femenino','Femenino'),('Masculino','Masculino'),('Autopercibido','Autopercibido')]
        self.marital_status.choices = [('0','Seleccione una opción...'),('Casado/a','Casado/a'),('Soltero/a','Soltero/a'),('Conviviente','Conviviente'),('Divorciado/a','Divorciado/a'),('Viudo/a','Viudo/a')]

    def saveModifyPersonData(self,uid,authorizer_id):
        """
        Actualización de datos en DB
        """
        with open_users_session() as session:
            persons = usersModel.get_users(session, [uid])
            if len(persons) == 1:
                person = persons[0]
                person.updated = datetime.datetime.utcnow()
                person.lastname = self.lastname.raw_data[0]
                person.firstname = self.firstname.raw_data[0]
                person.gender = self.gender.raw_data[0] if self.gender.raw_data[0] != '0' else None
                person.marital_status = self.marital_status.raw_data[0] if self.marital_status.raw_data[0] != '0' else None
                person.birthplace = self.birthplace.raw_data[0]
                person.birthdate = datetime.datetime.strptime(self.birthdate.raw_data[0],'%d-%m-%Y' ) if self.birthdate.raw_data[0] else None
                person.residence = self.residence.raw_data[0]
                person.address = self.address.raw_data[0]
                session.add(person)
                personLog = {  
                    'user' : {
                        'id': person.id,
                        'created': person.created,
                        'updated': person.updated,
                        'deleted': person.deleted,
                        'lastname': person.lastname,
                        'firstname': person.firstname,
                        'gender': person.gender,
                        'marital_status': person.marital_status,
                        'birthplace': person.birthplace,
                        'birthdate': person.birthdate,
                        'residence': person.residence,
                        'address': person.address,
                    }
                }
                newLog = UsersLog()
                newLog.entity_id = person.id
                newLog.authorizer_id = authorizer_id
                newLog.type = UserLogTypes.UPDATE
                newLog.data = json.dumps([personLog], default=str)
                session.add(newLog)
                session.commit()
                return 'Datos personales modificados'
            else:
                return 'Error interno'


class PersonIdNumberModifyForm(FlaskForm):
    person_number_type = SelectField('Tipo de Documento', coerce=str)
    person_number = StringField('Nro. de Documento', validators=[InputRequired()])
    
    def __init__(self):
        super(PersonIdNumberModifyForm,self).__init__()
        self.person_number_type.choices = [('0','Seleccione una opción...'),('DNI','DNI'),('LC','LC'),('LE','LE'),('PASSPORT','Pasaporte'),('CUIT','CUIT'),('CUIL','CUIL')]

    def validate_person_number_type(self, person_number_type):
        if self.person_number_type.raw_data[0] == '0':
            raise ValidationError('Debe seleccionar una opción')
    
    def saveModifyIdNumber(self,uid,authorizer_id):
        """
        Agregar documento
        """
        with open_users_session() as session:
            persons = usersModel.get_users(session, [uid])
            if len(persons) == 1:
                person = persons[0]
                if self.person_number.data and self.person_number_type.data:
                    if self.person_number_type.data != 'DNI' or self.person_number_type.data != 'LC' or self.person_number_type.data != 'LE':
                        idNumber = IdentityNumber()
                        idNumber.id = str(uuid.uuid4())
                        idNumber.created = datetime.datetime.utcnow()
                        idNumber.type = self.person_number_type.data
                        idNumber.number = self.person_number.data
                        idNumber.user_id = person.id
                        session.add(idNumber)
                        idNumberLog = {  
                            'identity_number': {
                                'id': idNumber.id,
                                'created': idNumber.created,
                                'updated': idNumber.updated,
                                'deleted': idNumber.deleted,
                                'type': idNumber.type,
                                'number': idNumber.number,
                                'user_id': idNumber.user_id,
                                'file_id': idNumber.file_id,
                                'file': idNumber.file_id
                            }
                        }
                        newLog = UsersLog()
                        newLog.entity_id = person.id
                        newLog.authorizer_id = authorizer_id
                        newLog.type = UserLogTypes.UPDATE
                        newLog.data = json.dumps([idNumberLog], default=str)
                        session.add(newLog)
                        session.commit()
                        return 'Documento agregado con éxito'
                    else:
                        return 'Error interno'


class PersonMailModifyForm(FlaskForm):
    email_type = SelectField('Tipo de correo electrónico', coerce=str)
    email = EmailField('Correo electrónico',  validators=[InputRequired()])
        
    def __init__(self):
        super(PersonMailModifyForm,self).__init__()
        self.email_type.choices = [('0','Seleccione una opción...'),('INSTITUTIONAL','Institucional'),('ALTERNATIVE','Personal')]

    def validate_email_type(self, email_type):
        if self.email_type.raw_data[0] == '0':
            raise ValidationError('Debe seleccionar una opción')
     
    def saveModifyMail(self,uid,authorizer_id):
        """ 
        Agregar correo personal
        """
        if (re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]*.unlp.edu.ar$",self.email.data)):
            return 'No está permitido agregar correo institucional'

        with open_users_session() as session:
            persons = usersModel.get_users(session, [uid])
            if len(persons) == 1:
                person = persons[0]
                if self.email.data and self.email_type.data == 'ALTERNATIVE':
                    newPersonalMail = Mail()
                    newPersonalMail.id = str(uuid.uuid4())
                    newPersonalMail.created = datetime.datetime.utcnow()
                    newPersonalMail.type = MailTypes.ALTERNATIVE
                    newPersonalMail.email = self.email.data
                    newPersonalMail.user_id = person.id
                    newPersonalMail.confirmed = datetime.datetime.utcnow()
                    session.add(newPersonalMail)
                    newPersonalMailLog = {  
                        'mail': {
                            'id': newPersonalMail.id,
                            'created': newPersonalMail.created,
                            'updated': newPersonalMail.updated,
                            'deleted': newPersonalMail.deleted,
                            'type': newPersonalMail.type,
                            'email': newPersonalMail.email,
                            'confirmed': newPersonalMail.confirmed,
                            'user_id': newPersonalMail.user_id,
                        }
                    }
                    newLog = UsersLog()
                    newLog.entity_id = person.id
                    newLog.authorizer_id = authorizer_id
                    newLog.type = UserLogTypes.UPDATE
                    newLog.data = json.dumps([newPersonalMailLog], default=str)
                    session.add(newLog)
                    session.commit()
                    return 'Correo agregado con éxito'
                else:
                    return 'Error'

class PersonPhoneModifyForm(FlaskForm):
    phone_type = SelectField('Tipo de número telefónico', coerce=str)
    phone_number =StringField('Número de teléfono', validators=[InputRequired()])
        
    def __init__(self):
        super(PersonPhoneModifyForm,self).__init__()
        self.phone_type.choices = [('0','Seleccione una opción...'),('CELLPHONE','Móvil'),('LANDLINE','Fijo')]

    def validate_phone_type(self, phone_type):
        if self.phone_type.data == '0':
            raise ValidationError('Debe seleccionar una opción')

    def saveModifyPhone(self,uid,authorizer_id):
        """
        Agregar teléfono
        """
        with open_users_session() as session:
            persons = usersModel.get_users(session, [uid])
            if len(persons) == 1:
                person = persons[0]
                if self.phone_number.data:
                    """ telefono fijo""" 
                    phoneToAdd = Phone()
                    phoneToAdd.id = str(uuid.uuid4())
                    phoneToAdd.created = datetime.datetime.utcnow()
                    if self.phone_type.data == 'LANDLINE':
                        phoneToAdd.type = PhoneTypes.LANDLINE
                    elif self.phone_type.data == 'CELLPHONE':
                        phoneToAdd.type = PhoneTypes.CELLPHONE
                    phoneToAdd.number = self.phone_number.data
                    phoneToAdd.user_id = person.id
                    session.add(phoneToAdd)
                    phoneToAddLog = {
                        'phone': {
                            'id': phoneToAdd.id,
                            'created': phoneToAdd.created,
                            'updated': phoneToAdd.updated,
                            'deleted': phoneToAdd.deleted,
                            'type': phoneToAdd.type,
                            'number': phoneToAdd.number,
                            'user_id': phoneToAdd.user_id,
                        }   
                    }
                    newLog = UsersLog()
                    newLog.entity_id = person.id
                    newLog.authorizer_id = authorizer_id
                    newLog.type = UserLogTypes.UPDATE
                    newLog.data = json.dumps([phoneToAddLog], default=str)
                    session.add(newLog)
                    session.commit()
                    return 'Teléfono agregado con exito'
                else:
                    return 'Error interno'
                    

class PersonSeniorityModifyForm(FlaskForm):
    seniority_external_years = StringField('Años')
    seniority_external_months = StringField('Meses')
    seniority_external_days = StringField('Días')
    personSeniorityModify = SubmitField('Guardar')
 
    def validate_seniority_external_years(self,seniority_external_years):
        if self.seniority_external_years.data:
            try:
                number = int(self.seniority_external_years.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor o igual 0')
    
    def validate_seniority_external_months(self,seniority_external_months):
        if self.seniority_external_months.data:
            try:
                number = int(self.seniority_external_months.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor o igual a 0')
            if number > 11:
                raise ValidationError('Utilice un número entre 0 y 11')
    
    def validate_seniority_external_days(self,seniority_external_days):
        if self.seniority_external_days.data:
            try:
                number = int(self.seniority_external_days.data)
            except:
                raise ValidationError('La antiguedad debe ser un número')
            if number < 0:
                raise ValidationError('El número debe ser mayor o igual a 0')
            if number > 29:
                raise ValidationError('Utilice un número entre 0 y 29')
                
    def saveModifySeniority(self,uid,authorizer_id):
        with open_sileg_session() as sileg_session:
            if (self.seniority_external_years.raw_data[0] or self.seniority_external_months.raw_data[0] or self.seniority_external_days.raw_data[0]) and (self.seniority_external_years.raw_data[0] != '0' or self.seniority_external_months.raw_data[0] != '0' or self.seniority_external_days.raw_data[0] != '0'):
                newSeniority = {
                    'seniority_external_years' : int(self.seniority_external_years.raw_data[0]) if self.seniority_external_years.raw_data[0] else 0,
                    'seniority_external_months'  : int(self.seniority_external_months.raw_data[0]) if self.seniority_external_months.raw_data[0] else 0,
                    'seniority_external_days' : int(self.seniority_external_days.raw_data[0]) if self.seniority_external_days.raw_data[0] else 0
                }
                external_seniority = ExternalSeniority()
                external_seniority.id = str(uuid.uuid4())
                external_seniority.created = datetime.datetime.utcnow()
                external_seniority.user_id = uid
                external_seniority.years = newSeniority['seniority_external_years']
                external_seniority.months = newSeniority['seniority_external_months']
                external_seniority.days = newSeniority['seniority_external_days']
                sileg_session.add(external_seniority)
                external_seniority_log = {  
                    'external_seniority' : {
                        'id': external_seniority.id,
                        'created': external_seniority.created,
                        'updated': external_seniority.updated,
                        'deleted': external_seniority.deleted,
                        'days': external_seniority.days,
                        'months': external_seniority.months,
                        'years': external_seniority.years,
                        'user_id': external_seniority.user_id
                    }
                }
                log = SilegLog()
                log.type = SilegLogTypes.CREATE
                log.entity_id = external_seniority.id
                log.authorizer_id = authorizer_id
                log.data = json.dumps([external_seniority_log], default=str)
                sileg_session.add(log)
            es_id = silegModel.get_external_seniority_by_user(sileg_session, uid)
            if es_id:
                es = silegModel.get_external_seniority(sileg_session, es_id)
                if es and len(es) >= 1 and not es[0].deleted:
                    toDelete_external_seniority = es[0]
                    toDelete_external_seniority.updated = datetime.datetime.utcnow()
                    toDelete_external_seniority.deleted = datetime.datetime.utcnow()
                    sileg_session.add(toDelete_external_seniority)
                    external_seniority_log = {  
                        'external_seniority' : {
                            'id': toDelete_external_seniority.id,
                            'created': toDelete_external_seniority.created,
                            'updated': toDelete_external_seniority.updated,
                            'deleted': toDelete_external_seniority.deleted,
                            'days': toDelete_external_seniority.days,
                            'months': toDelete_external_seniority.months,
                            'years': toDelete_external_seniority.years,
                            'user_id': toDelete_external_seniority.user_id
                        }
                    }
                    toDelete_log = SilegLog()
                    toDelete_log.type = SilegLogTypes.DELETE
                    toDelete_log.entity_id = toDelete_external_seniority.id
                    toDelete_log.authorizer_id = authorizer_id
                    toDelete_log.data = json.dumps([external_seniority_log], default=str)
                    sileg_session.add(toDelete_log)
                    try:
                        sileg_session.commit()
                        return 'Se ha modificado la antigüedad externa'
                    except:
                        return 'Error interno'
            try:
                sileg_session.commit()
                return 'Se ha modificado la antigüedad externa'
            except:
                return 'Error interno'
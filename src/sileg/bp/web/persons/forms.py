import json
import uuid
import base64
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, SelectField
from flask_wtf.file import FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email

from sileg.helpers.apiHandler import getStates
from sileg.helpers.namesHandler import id2sDegrees, id2sIdentityNumber

from sileg.models import usersModel, open_users_session
from users.model.entities.User import User, IdentityNumber, Mail, Phone, File, MailTypes, PhoneTypes, UsersLog, UserLogTypes, IdentityNumberTypes, DegreeTypes, UserDegree

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
                uid = str(uuid.uuid4())
                newUser = User()
                newUser.id = uid
                newUser.lastname = self.lastname.data
                newUser.firstname = self.firstname.data
                newUser.gender = self.gender.data if self.gender.data != '0' else None
                newUser.marital_status = self.marital_status.data if self.marital_status.data != '0' else None
                newUser.birthplace = self.birthplace.data
                newUser.birthdate = self.birthdate.data if self.birthdate.data else None
                newUser.residence = self.residence.data
                newUser.address = self.address.data
                session.add(newUser)
                toLog.append({  'id': newUser.id,
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
                                })

                """ Se carga archivo documento """
                person_file_id = None
                if self.person_numberFile.data:
                    person_file_id = str(uuid.uuid4())                    
                    personNumberFile = File()
                    personNumberFile.id = person_file_id
                    personNumberFile.mimetype = self.person_numberFile.data.mimetype
                    personNumberFile.content = base64.b64encode(self.person_numberFile.data.read()).decode()
                    session.add(personNumberFile)
                    toLog.append({  'id': personNumberFile.id,
                                    'created': personNumberFile.created,
                                    'updated': personNumberFile.updated,
                                    'deleted': personNumberFile.deleted,
                                    'mimetype': personNumberFile.mimetype,
                                    'content': personNumberFile.content,
                                })

                """ Se genera documento """
                idNumber = IdentityNumber()
                idNumber.type = self.person_number_type.data
                idNumber.number = self.person_number.data
                idNumber.user_id = uid
                if person_file_id:
                    idNumber.file_id = person_file_id
                session.add(idNumber)
                
                """ Se genera correo laboral """
                if self.work_email.data:
                    newWorkEmail = Mail()
                    newWorkEmail.type = MailTypes.INSTITUTIONAL
                    newWorkEmail.email = self.work_email.data
                    newWorkEmail.user_id = uid
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

                """ Se genera correo personal """
                if self.personal_email.data:
                    newPersonalMail = Mail()
                    newPersonalMail.type = MailTypes.NOTIFICATION
                    newPersonalMail.email = self.personal_email.data
                    newPersonalMail.user_id = uid
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

                """ Se genera telefono fijo """
                if self.land_line.data:
                    landLinePhone = Phone()
                    landLinePhone.type = PhoneTypes.LANDLINE
                    landLinePhone.number = self.land_line.data
                    landLinePhone.user_id = uid
                    session.add(landLinePhone)
                    toLog.append({  'id': landLinePhone.id,
                                    'created': landLinePhone.created,
                                    'updated': landLinePhone.updated,
                                    'deleted': landLinePhone.deleted,
                                    'type': landLinePhone.type.value,
                                    'number': landLinePhone.number,
                                    'user_id': landLinePhone.user_id,
                                })

                """ Se genera telefono movil """
                if self.mobile_number.data:
                    mobileNumber = Phone()
                    mobileNumber.type = PhoneTypes.CELLPHONE
                    mobileNumber.number = self.mobile_number.data
                    mobileNumber.user_id = uid
                    session.add(mobileNumber)
                    toLog.append({  'id': mobileNumber.id,
                                    'created': mobileNumber.created,
                                    'updated': mobileNumber.updated,
                                    'deleted': mobileNumber.deleted,
                                    'type': mobileNumber.type.value,
                                    'number': mobileNumber.number,
                                    'user_id': mobileNumber.user_id,
                                })

                if self.laboral_number.data:
                    cid = str(uuid.uuid4())
                    cuil = IdentityNumber()
                    cuil.id = cid
                    cuil.type = IdentityNumberTypes.CUIL
                    cuil.number = self.laboral_number.data
                    cuil.user_id = uid
                
                    """ Se genera archivo de cuil """
                    cfid = None
                    if self.laboral_numberFile.data:
                        cfid = str(uuid.uuid4())
                        laboralNumberFile = File()
                        laboralNumberFile.id = cfid
                        laboralNumberFile.mimetype = self.laboral_numberFile.data.mimetype
                        laboralNumberFile.content = base64.b64encode(self.laboral_numberFile.data.read()).decode()
                        session.add(laboralNumberFile)
                        toLog.append({  'id': laboralNumberFile.id,
                                        'created': laboralNumberFile.created,
                                        'updated': laboralNumberFile.updated,
                                        'deleted': laboralNumberFile.deleted,
                                        'mimetype': laboralNumberFile.mimetype,
                                        'content': laboralNumberFile.content,
                                        'identityNumber': cid,
                                    })
                    if cfid:
                        cuil.file_id = cfid
                    session.add(cuil)  

                newLog = UsersLog()
                newLog.entity_id = newUser.id
                newLog.authorizer_id = authorizer_id
                newLog.type = UserLogTypes.CREATE
                newLog.data = json.dumps(toLog, default=str)
                session.add(newLog)
                session.commit()

                """

                MODELO DE SILEG ---> ALTA DE ANTIGUEDAD DE PERSONA

                """
                #TODO Agregar a Sileg model la antiguedad de la persona
                newSeniority = {
                    'seniority_external_years' : self.seniority_external_years.data,
                    'seniority_external_months'  : self.seniority_external_months.data,
                    'seniority_external_days' : self.seniority_external_days.data
                }

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
        toLog = []
        with open_users_session() as session:
            if usersModel.get_users(session, [uid])[0]:
                """ Se carga archivo del titulo si existe """
                degree_file_id = None
                if self.degreeFile.data:
                    degree_file_id = str(uuid.uuid4())                    
                    degreeFile = File()
                    degreeFile.id = degree_file_id
                    degreeFile.mimetype = self.degreeFile.data.mimetype
                    degreeFile.content = base64.b64encode(self.degreeFile.data.read()).decode()
                    session.add(degreeFile)
                    toLog.append({  'id': degreeFile.id,
                                    'created': degreeFile.created,
                                    'updated': degreeFile.updated,
                                    'deleted': degreeFile.deleted,
                                    'mimetype': degreeFile.mimetype,
                                    'content': degreeFile.content,
                                })
                did = str(uuid.uuid4())
                newDegree = UserDegree()
                newDegree.id = did
                newDegree.type = self.degreeType.data
                newDegree.title = self.degreeName.data
                newDegree.start = self.degreeDate.data if self.degreeDate.data else None
                newDegree.user_id = uid
                if degree_file_id:
                    newDegree.file_id = degree_file_id
                session.add(newDegree)
                toLog.append({  'id': newDegree.id,
                                'created': newDegree.created,
                                'updated': newDegree.updated,
                                'deleted': newDegree.deleted,
                                'title': newDegree.title,
                                'start': newDegree.start,
                                'user_id': newDegree.user_id,
                            })                
                newLog = UsersLog()
                newLog.entity_id = did
                newLog.authorizer_id = authorizer_id
                newLog.type = UserLogTypes.CREATE
                newLog.data = json.dumps(toLog, default=str)
                session.add(newLog)
                session.commit()

class PersonSearchForm(FlaskForm):
    query = StringField('Buscar persona por apellido o número de documento')
    class Meta:
        csrf = False

class PersonModifyForm(FlaskForm):
    lastname = StringField('Apellidos', validators=[DataRequired()])
    firstname = StringField('Nombres', validators=[DataRequired()])
    person_number_type = SelectField('Tipo de Documento', coerce=str)
    person_number = StringField('Nro. de Documento', validators=[DataRequired()])
    gender = SelectField('Género', coerce=str)
    marital_status = SelectField('Estado Civil', coerce=str)
    birthplace = StringField('Ciudad de Nacimiento')
    birthdate = StringField('Fecha de Nacimiento')
    residence = StringField('Ciudad de Residencia')
    address = StringField('Dirección')
    work_email = EmailField('Correo de Trabajo')
    personal_email = EmailField('Correo Personal',validators=[DataRequired()])
    land_line = StringField('Teléfono Fijo')
    mobile_number =StringField('Teléfono Móvil')
    person_numberFile = FileField('Adjuntar DNI')
    laboral_number = StringField('CUIL')
    laboral_numberFile = FileField('Adjuntar CUIL')
    seniority_external_years = StringField('Años')
    seniority_external_months = StringField('Meses')
    seniority_external_days = StringField('Días')
        
    def __init__(self):
        super(PersonModifyForm,self).__init__()
        person_number_choices = [(id.value, id2sIdentityNumber(id)) for id in IdentityNumberTypes]
        person_number_choices.insert(0,('0','Seleccione una opción...'))
        self.person_number_type.choices = person_number_choices
        self.gender.choices = [('0','Seleccione una opción...'),('Femenino','Femenino'),('Masculino','Masculino'),('Autopercibido','Autopercibido')]
        self.marital_status.choices = [('0','Seleccione una opción...'),('Casado/a','Casado/a'),('Soltero/a','Soltero/a'),('Conviviente','Conviviente'),('Divorciado/a','Divorciado/a'),('Viudo/a','Viudo/a')]

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
                uid = str(uuid.uuid4())
                newUser = User()
                newUser.id = uid
                newUser.lastname = self.lastname.data
                newUser.firstname = self.firstname.data
                newUser.gender = self.gender.data if self.gender.data != '0' else None
                newUser.marital_status = self.marital_status.data if self.marital_status.data != '0' else None
                newUser.birthplace = self.birthplace.data
                newUser.birthdate = self.birthdate.data if self.birthdate.data else None
                newUser.residence = self.residence.data
                newUser.address = self.address.data
                session.add(newUser)
                toLog.append(newUser)

                """ Se carga archivo DNI """
                person_file_id = None
                if self.person_numberFile.data:
                    person_file_id = str(uuid.uuid4())                    
                    personNumberFile = File()
                    personNumberFile.id = person_file_id
                    personNumberFile.mimetype = self.person_numberFile.data.mimetype
                    personNumberFile.content = base64.b64encode(self.person_numberFile.data.read()).decode()
                    session.add(personNumberFile)
                    toLog.append({  'id': personNumberFile.id,
                                    'created': personNumberFile.created,
                                    'updated': personNumberFile.updated,
                                    'deleted': personNumberFile.deleted,
                                    'mimetype': personNumberFile.mimetype,
                                    'content': personNumberFile.content,
                                })

                """ Se genera DNI """
                idNumber = IdentityNumber()
                idNumber.type = self.person_number_type.data
                idNumber.number = self.person_number.data
                idNumber.user_id = uid
                if person_file_id:
                    idNumber.file_id = person_file_id
                session.add(idNumber)
                
                """ Se genera correo laboral """
                if self.work_email.data:
                    newWorkEmail = Mail()
                    newWorkEmail.type = MailTypes.INSTITUTIONAL
                    newWorkEmail.email = self.work_email.data
                    newWorkEmail.user_id = uid
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

                """ Se genera correo personal """
                if self.personal_email.data:
                    newPersonalMail = Mail()
                    newPersonalMail.type = MailTypes.ALTERNATIVE
                    newPersonalMail.email = self.personal_email.data
                    newPersonalMail.user_id = uid
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

                """ Se genera telefono fijo """
                if self.land_line.data:
                    landLinePhone = Phone()
                    landLinePhone.type = PhoneTypes.LANDLINE
                    landLinePhone.number = self.land_line.data
                    landLinePhone.user_id = uid
                    session.add(landLinePhone)
                    toLog.append({  'id': landLinePhone.id,
                                    'created': landLinePhone.created,
                                    'updated': landLinePhone.updated,
                                    'deleted': landLinePhone.deleted,
                                    'type': landLinePhone.type.value,
                                    'number': landLinePhone.number,
                                    'user_id': landLinePhone.user_id,
                                })

                """ Se genera telefono movil """
                if self.mobile_number.data:
                    mobileNumber = Phone()
                    mobileNumber.type = PhoneTypes.CELLPHONE
                    mobileNumber.number = self.mobile_number.data
                    mobileNumber.user_id = uid
                    session.add(mobileNumber)
                    toLog.append({  'id': mobileNumber.id,
                                    'created': mobileNumber.created,
                                    'updated': mobileNumber.updated,
                                    'deleted': mobileNumber.deleted,
                                    'type': mobileNumber.type.value,
                                    'number': mobileNumber.number,
                                    'user_id': mobileNumber.user_id,
                                })
               
                """ Se genera archivo de cuil """
                cid = None
                if self.laboral_numberFile.data:
                    cid = str(uuid.uuid4())
                    laboralNumberFile = File()
                    laboralNumberFile.id = cid
                    laboralNumberFile.mimetype = self.laboral_numberFile.data.mimetype
                    laboralNumberFile.content = base64.b64encode(self.laboral_numberFile.data.read()).decode()
                    session.add(laboralNumberFile)
                    toLog.append({  'id': laboralNumberFile.id,
                                    'created': laboralNumberFile.created,
                                    'updated': laboralNumberFile.updated,
                                    'deleted': laboralNumberFile.deleted,
                                    'mimetype': laboralNumberFile.mimetype,
                                    'type': laboralNumberFile.type.value,
                                    'content': laboralNumberFile.content,
                                    'user_id': laboralNumberFile.user_id,
                                })
                if self.laboral_number.data:
                    cuil = IdentityNumber()
                    cuil.type = IdentityNumberTypes.CUIL
                    cuil.number = self.laboral_number.data
                    cuil.user_id = uid
                    if cid:
                        cuil.file_id = cid
                    session.add(cuil)                        

                newLog = UsersLog()
                newLog.entity_id = newUser.id
                newLog.authorizer_id = authorizer_id
                newLog.type = UserLogTypes.CREATE
                newLog.data = json.dumps(toLog, default=str)
                session.add(newLog)
                session.commit()
                

        #TODO Agregar a Sileg model la antiguedad de la persona
        newSeniority = {
            'seniority_external_years' : self.seniority_external_years.data,
            'seniority_external_months'  : self.seniority_external_months.data,
            'seniority_external_days' : self.seniority_external_days.data
        }
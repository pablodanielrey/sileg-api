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

from sileg.models import usersModel, open_users_session
from users.model.entities.User import User, IdentityNumber, Mail, Phone, File, MailTypes, PhoneTypes, UsersLog, UserLogTypes, IdentityNumberTypes, DegreeTypes, UserDegree

class StudentCreateForm(FlaskForm):
    """

    MODELO DE USUARIOS
    
    """
    lastname = StringField('Apellidos', validators=[DataRequired()])
    firstname = StringField('Nombres', validators=[DataRequired()])
    person_number_type = SelectField('Tipo de Documento', coerce=str)
    person_number = StringField('Nro. de Documento', validators=[DataRequired()])
        
    def __init__(self):
        super(StudentCreateForm,self).__init__()
        self.person_number_type.choices = [('0','Seleccione una opción...'),('DNI','DNI'),('LC','LC'),('LE','LE'),('PASSPORT','Pasaporte')]

    def validate_person_number_type(self, person_number_type):
        if self.person_number_type.data == '0':
            raise ValidationError('Debe seleccionar una opción')   

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
                session.add(newUser)
                toLog.append({  'id': newUser.id,
                                'created': newUser.created,
                                'updated': newUser.updated,
                                'deleted': newUser.deleted,
                                'lastname': newUser.lastname,
                                'firstname': newUser.firstname
                                })

                """ Se genera documento """
                idNumber = IdentityNumber()
                idNumber.type = self.person_number_type.data
                idNumber.number = self.person_number.data
                idNumber.user_id = uid
                session.add(idNumber)
                toLog.append({  'id': idNumber.id,
                                    'created': idNumber.created,
                                    'updated': idNumber.updated,
                                    'deleted': idNumber.deleted,
                                    'type': idNumber.type,
                                    'number': idNumber.number,
                                    'user_id': idNumber.user_id,
                                })
                

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
                return self.person_number.data
            else:
                return None


class StudentDataModifyForm(FlaskForm):

    """
        TODO: todo esto no lo toque. es una copia de persona. hace falta modificarlo
    """

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
        super(StudentDataModifyForm,self).__init__()
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
                person.lastname = self.lastname.raw_data[0]
                person.firstname = self.firstname.raw_data[0]
                person.gender = self.gender.raw_data[0] if self.gender.raw_data[0] != '0' else None
                person.marital_status = self.marital_status.raw_data[0] if self.marital_status.raw_data[0] != '0' else None
                person.birthplace = self.birthplace.raw_data[0]
                person.birthdate = datetime.datetime.strptime(self.birthdate.raw_data[0],'%d-%m-%Y' ) if self.birthdate.raw_data[0] else None
                person.residence = self.residence.raw_data[0]
                person.address = self.address.raw_data[0]
                session.add(person)
                personLog = {  'id': person.id,
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
                newLog = UsersLog()
                newLog.entity_id = person.id
                newLog.authorizer_id = authorizer_id
                newLog.type = UserLogTypes.UPDATE
                newLog.data = json.dumps(personLog, default=str)
                session.add(newLog)
                session.commit()
                return 'Datos personales modificados'
            else:
                return 'Error interno'


class StudentIdNumberModifyForm(FlaskForm):
    person_number_type = SelectField('Tipo de Documento', coerce=str)
    person_number = StringField('Nro. de Documento', validators=[InputRequired()])
    
    def __init__(self):
        super(StudentIdNumberModifyForm,self).__init__()
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
                        idNumber.type = self.person_number_type.data
                        idNumber.number = self.person_number.data
                        idNumber.user_id = person.id
                        session.add(idNumber)
                        idNumberLog = {  'id': idNumber.id,
                                'created': idNumber.created,
                                'updated': idNumber.updated,
                                'deleted': idNumber.deleted,
                                'type': idNumber.type,
                                'number': idNumber.number,
                                'user_id': idNumber.user_id,
                                'file_id': idNumber.file_id,
                                'file': idNumber.file_id
                                }
                        newLog = UsersLog()
                        newLog.entity_id = person.id
                        newLog.authorizer_id = authorizer_id
                        newLog.type = UserLogTypes.UPDATE
                        newLog.data = json.dumps(idNumberLog, default=str)
                        session.add(newLog)
                        session.commit()
                        return 'Documento agregado con éxito'
                    else:
                        return 'Error interno'

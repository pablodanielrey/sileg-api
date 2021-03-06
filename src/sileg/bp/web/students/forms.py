import json
import uuid
import base64
import datetime
import re
import csv
import io

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField, SelectField, SubmitField
from flask_wtf.file import FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email, InputRequired

from sileg.helpers.apiHandler import getStates
from sileg.helpers.namesHandler import id2sDegrees, id2sIdentityNumber

from sileg.models import usersModel, open_users_session, loginModel, open_login_session
from users.model.entities.User import User, IdentityNumber, Mail, Phone, File, MailTypes, PhoneTypes, UsersLog, UserLogTypes, IdentityNumberTypes, DegreeTypes, UserDegree

class StudentCreateForm(FlaskForm):
    """

    MODELO DE USUARIOS
    
    """
    lastname = StringField('Apellidos', validators=[DataRequired()])
    firstname = StringField('Nombres', validators=[DataRequired()])
    person_number_type = SelectField('Tipo de Documento', coerce=str)
    person_number = StringField('Nro. de Documento', validators=[DataRequired()])
    student_number = StringField('Legajo (Opcional)')
        
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
        toLog = {}
        with open_users_session() as session:
            aux = usersModel.get_uid_person_number(session, self.person_number.data)
            if aux:
                return None

            if self.student_number.data:
                aux = usersModel.get_uid_person_student(session, self.student_number.data)
                if aux:
                    return None

            uid = str(uuid.uuid4())
            newUser = User()
            newUser.id = uid
            newUser.created = datetime.datetime.utcnow()
            newUser.lastname = self.lastname.data
            newUser.firstname = self.firstname.data
            session.add(newUser)
            toLog['user'] = {
                    'id': newUser.id,
                    'created': newUser.created,
                    'updated': newUser.updated,
                    'deleted': newUser.deleted,
                    'lastname': newUser.lastname,
                    'firstname': newUser.firstname
            }

            """ Se genera documento """
            idNumber = IdentityNumber()
            idNumber.id = str(uuid.uuid4())
            idNumber.created = datetime.datetime.utcnow()
            idNumber.type = self.person_number_type.data
            idNumber.number = self.person_number.data
            idNumber.user_id = uid
            session.add(idNumber)
            toLog['identity_number'] = {
                    'id': idNumber.id,
                    'created': idNumber.created,
                    'updated': idNumber.updated,
                    'deleted': idNumber.deleted,
                    'type': idNumber.type,
                    'number': idNumber.number,
                    'user_id': idNumber.user_id,
            }
            
            if self.student_number.data:
                s_number = IdentityNumber()
                s_number.id = str(uuid.uuid4())
                s_number.created = datetime.datetime.utcnow()
                s_number.type = IdentityNumberTypes.STUDENT
                s_number.number = self.student_number.data
                s_number.user_id = uid
                session.add(s_number)
                toLog['identity_number'] = {
                        'id': s_number.id,
                        'created': s_number.created,
                        'updated': s_number.updated,
                        'deleted': s_number.deleted,
                        'type': s_number.type,
                        'number': s_number.number,
                        'user_id': s_number.user_id,
                }

            newLog = UsersLog()
            newLog.entity_id = newUser.id
            newLog.authorizer_id = authorizer_id
            newLog.type = UserLogTypes.CREATE
            newLog.data = json.dumps([toLog], default=str)
            session.add(newLog)
            session.commit()
            return self.person_number.data


class StudentCSVCreateForm(FlaskForm):
    newFile = FileField('Adjuntar Archivo CSV',validators=[DataRequired()])

    def save(self, authorizer_id):
        try:
            checkStudentNumber = re.compile('\d+\/\d+')
            checkIdentityNumber = re.compile('^[0-9]+$')
            response = []
            csv_file = io.TextIOWrapper(self.newFile.data, encoding='utf-8-sig')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                with open_users_session() as session:
                    toLog = []
                    status = ''

                    identityNumber = row['dni'].replace(' ','')
                    if not checkIdentityNumber.match(identityNumber):
                        status = 'Error en formato de DNI'
                    firstname = row['nombres'].strip()
                    lastname = row['apellidos'].strip()
                    password = row['clave'].replace(' ','')
                    studentNumber = row['legajo'] if 'legajo' in row else None
                    studentNumber = studentNumber.replace(' ','') if studentNumber else None
                    if studentNumber and not checkStudentNumber.match(studentNumber):
                        status = 'Error en formato de Legajo'

                    if status == '':
                        aux = usersModel.get_uid_person_number(session, identityNumber)
                        if aux:
                            status = 'La persona ya existe'
                        else:
                            uid = str(uuid.uuid4())
                            newUser = User()
                            newUser.id = uid
                            newUser.created = datetime.datetime.utcnow()
                            newUser.lastname = lastname
                            newUser.firstname = firstname
                            session.add(newUser)
                            toLog.append({
                                    'id': newUser.id,
                                    'created': newUser.created,
                                    'updated': newUser.updated,
                                    'deleted': newUser.deleted,
                                    'lastname': newUser.lastname,
                                    'firstname': newUser.firstname
                            })

                            """ Se genera documento """
                            idNumber = IdentityNumber()
                            idNumber.id = str(uuid.uuid4())
                            idNumber.created = datetime.datetime.utcnow()
                            idNumber.type = IdentityNumberTypes.DNI
                            idNumber.number = identityNumber
                            idNumber.user_id = uid
                            session.add(idNumber)
                            toLog.append({
                                    'id': idNumber.id,
                                    'created': idNumber.created,
                                    'updated': idNumber.updated,
                                    'deleted': idNumber.deleted,
                                    'type': idNumber.type,
                                    'number': idNumber.number,
                                    'user_id': idNumber.user_id,
                            })
                            """ Se genera legajo solamente si esta cargado """
                            if studentNumber:
                                newStudentNumber = IdentityNumber()
                                newStudentNumber.id = str(uuid.uuid4())
                                newStudentNumber.created = datetime.datetime.utcnow()
                                newStudentNumber.type = IdentityNumberTypes.STUDENT
                                newStudentNumber.number = studentNumber
                                newStudentNumber.user_id = uid
                                session.add(newStudentNumber)
                                toLog.append({
                                        'id': newStudentNumber.id,
                                        'created': newStudentNumber.created,
                                        'updated': newStudentNumber.updated,
                                        'deleted': newStudentNumber.deleted,
                                        'type': newStudentNumber.type,
                                        'number': newStudentNumber.number,
                                        'user_id': newStudentNumber.user_id,
                                })
                            for log in toLog:
                                newLog = UsersLog()
                                newLog.entity_id = newUser.id
                                newLog.authorizer_id = authorizer_id
                                newLog.type = UserLogTypes.CREATE
                                newLog.data = json.dumps([log], default=str)
                                session.add(newLog)
                            try:
                                session.commit()
                                pass
                            except:
                                status = 'Error al guardar persona'

                            if status == '':
                                try:
                                    with open_login_session() as loginSession:
                                        credentials = loginModel.change_credentials(loginSession, uid, identityNumber, password)
                                        loginSession.commit()
                                except:
                                    status = 'Persona Creada, Error al crear clave'

                response.append({
                    'identityNumber': identityNumber,
                    'firstname': firstname,
                    'lastname': lastname,
                    'status': status if status != '' else 'Creado Correctamente'
                })
            return response
        except:
            return []
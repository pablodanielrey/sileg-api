import uuid
import re
import json
import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired

from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.Place import Place, PlaceTypes
from sileg_model.model.entities.Log import SilegLog, SilegLogTypes

silegModel = SilegModel()

def placeTypeToString(p:PlaceTypes):
    if p == PlaceTypes.UNIVERSIDAD:
        return 'Universidad'
    if p == PlaceTypes.FACULTAD:
        return 'Facultad'
    if p == PlaceTypes.SECRETARIA:
        return 'Secretaría'
    if p == PlaceTypes.PROSECRETARIA:
        return 'Pro-Secretaría'
    if p == PlaceTypes.DEPARTAMENTO:
        return 'Departamento'
    if p == PlaceTypes.DIRECCION:
        return 'Dirección'
    if p == PlaceTypes.INSTITUTO:
        return 'Instituto'
    if p == PlaceTypes.ESCUELA:
        return 'Escuela'
    if p == PlaceTypes.SEMINARIO:
        return 'Seminario'
    if p == PlaceTypes.AREA:
        return 'Area'
    if p == PlaceTypes.DIVISION:
        return 'División'
    if p == PlaceTypes.MAESTRIA:
        return 'Maestría'
    if p == PlaceTypes.CENTRO:
        return 'Centro'
    if p == PlaceTypes.MATERIA:
        return 'Materia'
    if p == PlaceTypes.CATEDRA:
        return 'Catedra'

class PlaceCreateForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    type = SelectField('Tipo', coerce=str)
    description = StringField('Descripción')
    number = StringField('Número')
    telephone = StringField('Teléfono')
    email = EmailField('Correo electrónico')
        
    def __init__(self):
        super(PlaceCreateForm,self).__init__()
        typeChoices = [(d.value, placeTypeToString(d)) for d in PlaceTypes ]
        typeChoices.insert(0,('0','Seleccione una opción...'))
        self.type.choices = typeChoices
        
    def validate_email(self, email):
        if self.email.data and self.email.data != '':
            if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]*econo.unlp.edu.ar$",self.email.data) == None:
                raise ValidationError('El correo ingresado es erroneo.')

    def save(self,session,authorizer_id):
        """
        Persistencia de datos en DB
        """
        pid = str(uuid.uuid4())
        newPlace = Place()
        newPlace.id = pid
        newPlace.created = datetime.datetime.utcnow()
        newPlace.name = self.name.data
        newPlace.type = self.type.data
        newPlace.description = self.description.data
        newPlace.number = self.number.data
        newPlace.telephone = self.telephone.data
        newPlace.email = self.email.data
        session.add(newPlace)
        toLog = {
                'place' : {
                    'id': newPlace.id,
                    'created': newPlace.created,
                    'updated': newPlace.updated,
                    'deleted': newPlace.deleted,
                    'name': newPlace.name,
                    'type': newPlace.type,
                    'description': newPlace.description,
                    'number': newPlace.number,
                    'telephone': newPlace.telephone,
                    'email': newPlace.email,
                }
        }
        newLog = SilegLog()
        newLog.entity_id = newPlace.id
        newLog.authorizer_id = authorizer_id
        newLog.type = SilegLogTypes.CREATE
        newLog.data = json.dumps(toLog, default=str)
        session.add(newLog)

class PlaceModifyForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    type = SelectField('Tipo', coerce=str)
    description = StringField('Descripción')
    number = StringField('Número')
    telephone = StringField('Teléfono')
    email = EmailField('Correo electrónico')
        
    def __init__(self,session=None,pid=None):
        super(PlaceModifyForm,self).__init__()
        typeChoices = [(d.value, placeTypeToString(d)) for d in PlaceTypes ]
        typeChoices.insert(0,('0','Seleccione una opción...'))
        self.type.choices = typeChoices
        if session and pid:
            places = silegModel.get_places(session,[pid])
            if places and len(places) == 1:
                place = places[0]
                self.type.default = place.type.value
                self.process()
                self.name.data = place.name
                self.description.data = place.description
                self.number.data = place.number
                self.telephone.data = place.number
                self.email.data = place.email      
        
    def validate_email(self, email):
        if self.email.data and self.email.data != '':
            if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-.]*econo.unlp.edu.ar$",self.email.data) == None:
                raise ValidationError('El correo ingresado es erroneo.')

    def save(self,session,pid,authorizer_id):
        """
        Persistencia de datos en DB
        """
        places = silegModel.get_places(session,[pid])
        if places and len(places) == 1 and not places[0].deleted:
            place = places[0]
            place.updated = datetime.datetime.utcnow()
            place.name = self.name.data
            place.type = self.type.data
            place.description = self.description.data
            place.number = self.number.data
            place.telephone = self.telephone.data
            place.email = self.email.data
            session.add(place)
            toLog = {'place' : {
                    'id': place.id,
                    'created': place.created,
                    'updated': place.updated,
                    'deleted': place.deleted,
                    'name': place.name,
                    'type': place.type,
                    'description': place.description,
                    'number': place.number,
                    'telephone': place.telephone,
                    'email': place.email,
                    }
            }
            newLog = SilegLog()
            newLog.entity_id = place.id
            newLog.authorizer_id = authorizer_id
            newLog.type = SilegLogTypes.UPDATE
            newLog.data = json.dumps(toLog, default=str)
            session.add(newLog)
            return place.id
        else:
            return None

class PlaceSearchForm(FlaskForm):
    query = StringField('Buscar lugar')
    class Meta:
        csrf = False        


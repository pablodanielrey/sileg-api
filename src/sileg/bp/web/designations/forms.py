import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, EqualTo

from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.Designation import Designation, DesignationTypes

class DesignationCreateForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    #start = DateTimeField('Fecha Desde', validators=[DataRequired()])
    start = DateTimeField('Fecha Desde')
    end = DateTimeField('Fecha Hasta')

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Suplente
    # aca hay que buscar alguna forma de seleccionar designaciones a las cual les realiza la suplencia.
    #replace = SelectField('Reemplaza a', coerce=str)

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [
            ('0','Indeterminado..'),
            ('0','Fecha de Finalización'),
            ('0','Hasta concurso'),
            ('0','Hasta convalidación Consejo Superior'),
            ('0','Hasta nuevo llamado'),
            ('0','Fin de Suplencia')
        ]
        
    def save(self, session, silegModel, uid):
        d = Designation()
        d.type = DesignationTypes.ORIGINAL
        d.user_id = uid

        d.start = self.start.data
        d.end = self.end.data
        d.function_id = self.function.data
        d.place_id = self.place.data
        
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        
        session.add(d)


class ReplacementDesignationCreateForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    #start = DateTimeField('Fecha Desde', validators=[DataRequired()])
    start = DateTimeField('Fecha Desde')
    end = DateTimeField('Fecha Hasta')

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [
            ('0','Fin de Suplencia')
        ]
        
    def save(self, session, silegModel, uid, replaced_did):
        d = Designation()
        d.type = DesignationTypes.REPLACEMENT
        d.designation_id = replaced_did
        
        d.start = self.start.data
        d.end = self.end.data
        d.function_id = self.function.data
        d.place_id = self.place.data
        d.user_id = uid
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        session.add(d)


class ConvalidateDesignationForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    #start = DateTimeField('Fecha Desde', validators=[DataRequired()])
    start = DateTimeField('Fecha Desde')
    end = DateTimeField('Fecha Hasta')

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [
            ('0','Indeterminado..'),
            ('0','Fecha de Finalización'),
            ('0','Hasta concurso'),
            ('0','Hasta nuevo llamado')
        ]
        
    def save(self, session, replaced_designation: Designation):
        replaced_designation.deleted = datetime.datetime.now()
        replaced_designation.historic = True

        d = Designation()
        d.type = DesignationTypes.ORIGINAL
        d.designation_id = replaced_designation.id
        d.user_id = replaced_designation.user_id
        d.place_id = replaced_designation.place_id
        
        d.start = self.start.data
        d.end = self.end.data
        d.function_id = self.function.data
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        session.add(d)


class PromoteDesignationForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    #start = DateTimeField('Fecha Desde', validators=[DataRequired()])
    start = DateTimeField('Fecha Desde')
    end = DateTimeField('Fecha Hasta')

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [
            ('0','Indeterminado..'),
            ('0','Fecha de Finalización'),
            ('0','Hasta concurso'),
            ('0','Hasta nuevo llamado')
        ]
        
    def save(self, session, designation: Designation):
        d = Designation()
        d.type = DesignationTypes.PROMOTION
        d.designation_id = designation.id
        d.user_id = designation.user_id
        
        d.start = self.start.data
        d.end = self.end.data
        d.function_id = self.function.data
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        d.place_id = self.place.data
        session.add(d)


class ExtendDesignationForm(FlaskForm):
    # Datos del cargo
    function = SelectField('Cargo', coerce=str)
    functionEndType = SelectField('Finaliza', coerce=str)

    #start = DateTimeField('Fecha Desde', validators=[DataRequired()])
    start = DateTimeField('Fecha Desde')
    end = DateTimeField('Fecha Hasta')

    res = StringField('Número de resolución')
    exp = StringField('Expediente')
    cor = StringField('Corresponde')

    place = SelectField('Ubicación',coerce=str)

    observations = StringField('Observaciones', widget=TextArea())

    # Ordenanza 174
    adjusted174 = BooleanField('Ajustada a 174')

    def __init__(self, session, silegModel):
        super().__init__()
        self._load_values(session, silegModel)

    def _load_values(self, session, silegModel: SilegModel):
        self.function.choices = [ (f.id, f.name) for f in silegModel.get_functions(session) ]
        self.place.choices = [ (p.id, p.name) for p in silegModel.get_places(session, pids=silegModel.get_all_places(session)) ]
        self.functionEndType.choices = [
            ('0','Indeterminado..'),
            ('0','Fecha de Finalización'),
            ('0','Hasta concurso'),
            ('0','Hasta nuevo llamado')
        ]
        
    def save(self, session, designation: Designation):
        d = Designation()
        d.type = DesignationTypes.EXTENSION
        d.designation_id = designation.id
        d.user_id = designation.user_id
        d.place_id = designation.place_id
        d.function_id = designation.function_id

        d.start = self.start.data
        d.end = self.end.data
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data

        session.add(d)


class DeleteDesignationForm(FlaskForm):

    def save(self, session, designation: Designation):
        designation.deleted = datetime.datetime.now()
        designation.historic = True


class DesignationSearchForm(FlaskForm):
    query = StringField('Buscar designaciones por nombre, apellido o número de documento')
    class Meta:
        csrf = False

class PersonSearchForm(FlaskForm):
    query = StringField('Buscar persona por apellido o número de documento')
    class Meta:
        csrf = False        


    
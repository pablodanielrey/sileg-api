from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, EqualTo

from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.Designation import Designation

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
        d.start = self.start.data
        d.end = self.end.data
        d.function_id = self.function.data
        d.place_id = self.place.data
        d.user_id = uid
        d.exp = self.exp.data
        d.res = self.res.data
        d.cor = self.cor.data
        session.add(d)


class ExtendDesignationForm(FlaskForm):
    newDedication = SelectField('Nueva Dedicación', coerce=str)
    dedicationFrom = DateTimeField('Fecha Desde', validators=[DataRequired()])
    dedicationTo = DateTimeField('Fecha Hasta', validators=[DataRequired()])
    resolutionNumber = StringField('Número de resolución')
    recordNumber = StringField('Expediente')
    relatedNumber = StringField('Corresponde')
    positionEndType = SelectField('Tipo Fin Cargo',coerce=str) 
    department = SelectField('Departamento')
    departmentArea = SelectField('Materia',coerce=str)
    chair = SelectField('Cátedra',coerce=str)
    commission = StringField('Comisión')
    workArea = SelectField('Area',coerce=str)
    workPlace = SelectField('Lugar de Trabajo',coerce=str)
    function = SelectField('Función',coerce=str)
    
    dischargeType = SelectField('Tipo de baja', coerce=str) 
    dischargeDate = DateTimeField('Fecha de baja', validators=[DataRequired()])

    dischargeResolution = StringField('Número de resolución')
    dischargeRecordNumber = StringField('Expediente')
    dischargeRelatedNumber = StringField('Corresponde')

    def __init__(self):
        super(ExtendDesignationForm,self).__init__()
        self.newDedication.choices = [('0','Seleccione una opción...'),('0','A-H'),('0','Exclusiva'),('0','Semidedicacion'),('0','Semiexclusiva'),('0','Simple'),('0','Tiempo Completo')]
        self.positionEndType.choices = [('0','Seleccione una opción...'),('0','Hasta Concurso...'),('0','Hasta Convalid. Consejo Superior'),('0','Hasta nuevo llamado')]
        self.department.choices = [('0','Seleccione una opción...')]
        self.departmentArea.choices = [('0','Seleccione una opción...')]
        self.chair.choices = [('0','Seleccione una opción...')]
        self.commission.choices = [('0','Seleccione una opción...')]
        self.workArea.choices = [('0','Seleccione una opción...')]
        self.workPlace.choices = [('0','Seleccione una opción...')]
        self.function.choices = [('0','Seleccione una opción...')]        
        self.dischargeType.choices = [('0','Seleccione una opción...'),('0','Cambio de Cátedra'),('0','Cambio de Licencia'),('0','Fallecimiento'),('0','Jubilación'),('0','Limitación de Cargo'),('0','Limitación de Funciones'),('0','Reintegro de Licencia'),('0','Renuncia'),('0','Término de Designación'),('0','Término de Extensión'),('0','Término de Licencia')]

class RenewForm(FlaskForm):
    acquisitionDate = DateTimeField('Fecha de Obtención', validators=[DataRequired()])
    dedicationFrom = DateTimeField('Fecha Desde', validators=[DataRequired()])
    dedicationTo = DateTimeField('Fecha Hasta', validators=[DataRequired()])
    resolutionNumber = StringField('Número de resolución')
    recordNumber = StringField('Expediente')
    relatedNumber = StringField('Corresponde')
    positionEndType = SelectField('Tipo Fin Cargo',coerce=str)
    
    dischargeType = SelectField('Tipo de baja', coerce=str) 
    dischargeDate = DateTimeField('Fecha de baja', validators=[DataRequired()])

    dischargeResolution = StringField('Número de resolución')
    dischargeRecordNumber = StringField('Expediente')
    dischargeRelatedNumber = StringField('Corresponde')

    def __init__(self):
        super(RenewForm,self).__init__()
        self.positionEndType.choices = [('0','Seleccione una opción...'),('0','Hasta Concurso...'),('0','Hasta Convalid. Consejo Superior'),('0','Hasta nuevo llamado')]
        self.dischargeType.choices = [('0','Seleccione una opción...'),('0','Cambio de Cátedra'),('0','Cambio de Licencia'),('0','Fallecimiento'),('0','Jubilación'),('0','Limitación de Cargo'),('0','Limitación de Funciones'),('0','Reintegro de Licencia'),('0','Renuncia'),('0','Término de Designación'),('0','Término de Extensión'),('0','Término de Licencia')]

class DesignationSearchForm(FlaskForm):
    query = StringField('Buscar designaciones por nombre, apellido o número de documento')
    class Meta:
        csrf = False

class PersonSearchForm(FlaskForm):
    query = StringField('Buscar persona por apellido o número de documento')
    class Meta:
        csrf = False        
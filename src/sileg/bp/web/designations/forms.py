from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateTimeField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, EqualTo


class DesignationCreateForm(FlaskForm):
    # Datos del cargo
    positionType = SelectField('Tipo de cargo',coerce=str)
    dedication = SelectField('Dedicación',coerce=str)
    character = SelectField('Carácter', coerce=str)
    extraordinary = SelectField('Extraordinario', coerce=str)
    designationFrom = DateTimeField('Fecha Desde', validators=[DataRequired()])
    designationTo = DateTimeField('Fecha Hasta')
    validatedBySuperiorCouncil = DateTimeField('Convalidado por Consejo Superior')
    resolutionNumber = StringField('Número de resolución')
    recordNumber = StringField('Expediente')
    relatedNumber = StringField('Corresponde')
    positionEndType = SelectField('Tipo Fin Cargo',coerce=str)
    observations = StringField('Observaciones', widget=TextArea())
    # Cargo docente
    place = SelectField('Departamento',coerce=str)
    subject = SelectField('Materia',coerce=str)
    chair = SelectField('Cátedra',coerce=str)
    commission = StringField('Comisión')
    # Cargo de planta
    workArea = SelectField('Area',coerce=str)
    workPlace = SelectField('Lugar de Trabajo',coerce=str)
    function = SelectField('Función',coerce=str)
    # Suplente
    replace = SelectField('Reemplaza a', coerce=str)
    # Ordenanza 174
    adjusted = BooleanField('Está ajustada')
    ordResolutionNumber = StringField('Número de resolución')
    ordRecordNumber = StringField('Expediente')
    ordRelatedNumber = StringField('Corresponde')
    ordFrom = DateTimeField('Fecha Desde')
    ordTo = DateTimeField('Fecha Hasta')
    # Datos de baja
    dischargeType = SelectField('Tipo de baja', coerce=str) 
    dischargeDate = DateTimeField('Fecha de baja')
    # Resolucion de baja
    dischargeResolutionNumber = StringField('Número de resolución')
    dischargeRecordNumber = StringField('Expediente')
    dischargeRelatedNumber = StringField('Corresponde')
    
    def __init__(self):
        super(DesignationCreateForm,self).__init__()
        self.positionType.choices = [('0','Seleccione una opción...'),('0','Adjunto'),('0','Asociado'),('0','Ayudante alumno'),('0','Ayudante diplomado'),('0','Decano'),('0','Vicedecano'),('0','Jefe auxiliares docentes'),('0','Prosecretario'),('0','Secretario'),('0','Titular')]
        self.dedication.choices = [('0','Seleccione una opción...'),('0','A-H'),('0','Exclusiva'),('0','Semidedicación'),('0','Semiexclusiva'),('0','Simple'),('0','Tiempo completo')]
        self.character.choices = [('0','Seleccione una opción...'),('0','Ad honorem'),('0','Interino'),('0','Ordinario'),('0','Suplente')]
        self.extraordinary.choices = [('0','Seleccione una opción...'),('0','Consulto'),('0','Emérito'),('0','Secretaría de control y planificación institucional'),('0','Visitante')]
        self.positionEndType.choices = [('0','Seleccione una opción...'),('0','Hasta concurso'),('0','Hasta convalid. Consejo Superior'),('0','Hasta nuevo llamado')]
        self.place.choices = [('0','Seleccione una opción...')]
        self.subject.choices = [('0','Seleccione una opción...')]
        self.chair.choices = [('0','Seleccione una opción...')]
        self.workArea.choices = [('0','Seleccione una opción...')]
        self.workPlace.choices = [('0','Seleccione una opción...')]
        self.function.choices = [('0','Seleccione una opción...')]
        self.replace.choices = [('0','Seleccione una opción...')]
        self.dischargeType.choices = [('0','Seleccione una opción...')]

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
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from model_utils import Base

class Cargo(Base):

    __tablename__ = 'cargo'

    nombre = Column(String)
    tipo = Column(String)
    descripcion = Column(String)
    old_id = Column(String)

    _tipos = [
        'Docente',
        'No Docente',
        'Autoridad',
        'Pre Grado',
        'Alumno',
        'Ingreso',
        'Indefinido'
    ]

    """
    __mapper_args__ = {
        'polymorphic_on':tipo,
        'polymorphic_identity':'cargo'
    }
    """

    def __init__(self, id=None, nombre = None, tipo = None, descripcion = '', old_id=None):
        if id: self.id = id
        if nombre: self.nombre = nombre
        if tipo: self.tipo = tipo
        self.descripcion = descripcion
        self.old_id = old_id


"""
class Docente(Cargo):

    __mapper_args__ = {
        'polymorphic_identity':'Docente'
    }


class DocentePreuniversitario(Cargo):

    __mapper_args__ = {        
        'polymorphic_identity':'Docente Preuniversitario'
    }


class Definir(Cargo):

    __mapper_args__ = {        
        'polymorphic_identity':'Definir'
    }
    

class NoDocente(Cargo):

    __mapper_args__ = {
        'polymorphic_identity':'No Docente'
    }


class AutoridadSuperior(Cargo):

    __mapper_args__ = {
        'polymorphic_identity':'Autoridad Superior'
    }


class BecaDeInvestigacion(Cargo):

    __mapper_args__ = {
        'polymorphic_identity':'Beca'
    }


class BecaExperienciaLaboral(Cargo):

    __mapper_args__ = {
        'polymorphic_identity':'Beca de Experiencia Laboral'
    }


class ContratoDeObra(Cargo):

    __mapper_args__ = {
        'polymorphic_identity':'Contrato de Obra'
    } 


class CumpleFunciones(NoDocente):

    def __init__(self):
        self.id = '245eae51-28c4-4c6b-9085-354606399666'
        self.nombre = 'Cumple Funciones'
"""
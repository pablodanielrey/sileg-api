from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from model_utils import Base

class Cargo(Base):

    __tablename__ = 'cargo'

    nombre = Column(String)
    tipo = Column(String)

    __mapper_args__ = {
        'polymorphic_on':tipo,
        'polymorphic_identity':'cargo'
    }



    """
        ejemplos de tipo
        Docente
        No Docente
        Beca
        Docente Preuniversitario
        Autoridad Superior
        Definir        
    """

    """
        ejemplos de cargos
        A7
        E7
        Titular
        Adjunto
        Adscripto
        Director
        E2
        A2
        Cumple Funciones
        Beca
        Contrato de Obra
        Contrato de Servicio
        Contrato de Gestión
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


class Beca(Cargo):

    __mapper_args__ = {
        'polymorphic_identity':'Beca'
    }    


class CumpleFunciones(NoDocente):

    def __init__(self):
        self.id = '245eae51-28c4-4c6b-9085-354606399666'
        self.nombre = 'Cumple Funciones'

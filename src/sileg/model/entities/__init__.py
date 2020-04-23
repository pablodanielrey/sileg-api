import uuid
from sqlalchemy import Column, String, DateTime, func, desc
from sqlalchemy.ext.declarative import declarative_base
from flask_jsontools import JsonSerializableBase

def generateId():
    return str(uuid.uuid4())

class MyBaseClass:

    id = Column(String, primary_key=True, default=generateId)
    creado = Column(DateTime, server_default=func.now())
    actualizado = Column(DateTime, onupdate=func.now())

    def __init__(self):
        self.id = generateId()

    @classmethod
    def findAll(cls, s):
        return s.query(cls).all()

Base = declarative_base(cls=(JsonSerializableBase,MyBaseClass))


from .Lugar import Catedra, Departamento, Lugar, LugarDictado, Secretaria, Instituto, Prosecretaria, Escuela, Maestria, Direccion, Centro, Facultad, Oficina, Division, Area, Categoria
from .Cargo import Cargo
from .Designacion import Designacion, CategoriaDesignacion, Caracter
from .Materia import Materia

__all__ = [
    'Catedra',
    'Centro',
    'Departamento',
    'Designacion',
    'CategoriaDesignacion',
    'Direccion',
    'Escuela',
    'Lugar',
    'LugarDictado',
    'Materia',
    'Secretaria',
    'Instituto',
    'Prosecretaria',
    'Maestria',
    'Facultad',
    'Area',
    'Division',
    'Categoria',
    'Cargo',
    'Oficina',
    'Caracter'
]

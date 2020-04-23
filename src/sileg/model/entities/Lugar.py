from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sileg.model.entities import Base, generateId


class Lugar(Base):
    __tablename__ = 'lugar'

    nombre = Column(String)
    tipo = Column(String)
    descripcion = Column(String)
    numero = Column(String)
    telefono = Column(String)
    correo = Column(String)
    eliminado = Column('eliminado', DateTime)

    padre_id = Column(String, ForeignKey('lugar.id'))
    hijos = relationship("Lugar",  foreign_keys=[padre_id], backref=backref('padre', remote_side="Lugar.id"))

    cambio_id = Column(String, ForeignKey('lugar.id'))
    cambios = relationship("Lugar",  foreign_keys=[cambio_id], backref=backref('cambio', remote_side="Lugar.id"))

    old_id = Column(String)

    __mapper_args__ = {
        'polymorphic_on':tipo,
        'polymorphic_identity':'lugar'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre

    @property
    def getNombre(self):
        return self.nombre

    @classmethod
    def find(cls, session):
        return session.query(cls)


class Catedra(Lugar):
    __tablename__ = 'catedra'

    id = Column(String, ForeignKey('lugar.id'), primary_key=True, default=generateId)
    materia_id = Column(String, ForeignKey('materia.id'))
    materia = relationship("Materia")

    def __init__(self, nombre, materia_id, padre_id):
        self.nombre = nombre
        self.materia_id = materia_id
        self.padre_id = padre_id

    @property
    def getNombre(self):
        return self.nombre + ' ' + self.materia.nombre

    __mapper_args__ = {
        'polymorphic_identity':'catedra'
    }


class LugarDictado(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'lugar dictado'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre    

class Centro(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'centro'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre    

class Comision(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'comision'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre    

class Departamento(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'departamento'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre    

class Direccion(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'direccion'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre

class Escuela(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'escuela'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Externo(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'externo'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Facultad(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'facultad'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Instituto(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'instituto'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Maestria(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'maestria'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Prosecretaria(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'prosecretaria'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Secretaria(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'secretaria'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Seminario(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'seminario'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Universidad(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'universidad'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre


class Oficina(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'oficina'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre    

class Division(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'division'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre    

class Area(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'area'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre    


class Categoria(Lugar):
    __mapper_args__ = {
        'polymorphic_identity':'categoria'
    }

    def __init__(self, id=None, nombre=None):
        if id: self.id = id
        if nombre: self.nombre = nombre    

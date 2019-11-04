from sqlalchemy import Column, String, Date, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from model_utils import Base

from .Cargo import Cargo
from .Lugar import Lugar

categoria_designacion_table = Table('categoria_designacion', Base.metadata,
    Column('designacion_id', String, ForeignKey('designacion.id')),
    Column('categoria_id', String, ForeignKey('categoria.id'))
)

class Caracter(Base):

    __tablename__ = 'caracter'

    nombre = Column(String, unique=True)

    old_id = Column(String)

class Designacion(Base):

    __tablename__ = 'designacion'

    desde = Column(Date)
    hasta = Column(Date)
    historico = Column(Boolean)

    expediente = Column(String)
    resolucion = Column(String)
    corresponde = Column(String)

    tipo = Column(String)
    categorias = relationship('CategoriaDesignacion', secondary=categoria_designacion_table, back_populates='designaciones')

    designacion_id = Column(String, ForeignKey('designacion.id'))
    designacion = relationship('Designacion', foreign_keys=[designacion_id])
    #designacion = relationship('Designacion', back_populates='designaciones')

    #designaciones = relationship('Designacion', back_populates='designacion')

    usuario_id = Column(String)

    cargo_id = Column(String, ForeignKey('cargo.id'))
    cargo = relationship('Cargo', back_populates='designaciones')

    lugar_id = Column(String, ForeignKey('lugar.id'))
    lugar = relationship('Lugar', back_populates='designaciones')

    caracter_id = Column(String, ForeignKey('caracter.id'))
    #caracter = relationship('Caracter', back_populates='tipos_caracter')

    observaciones = Column(String)

    old_id = Column(String)

    """
    _mapper_args__ = {
        'polymorphic_on':tipo,
        'polymorphic_identity':'designacion'
    }
    """


    @classmethod
    def find(cls, session):
        query = session.query(cls).join(Designacion.lugar).join(Designacion.cargo)
        return query

Cargo.designaciones = relationship('Designacion', back_populates='cargo')
Lugar.designaciones = relationship('Designacion', back_populates='lugar')


"""
class BajaDesignacion(Designacion):
    __mapper_args__ = {
        'polymorphic_identity':'baja'
    }
"""

class CategoriaDesignacion(Base):

    __tablename__ = 'categoria'

    nombre = Column(String, unique=True)

    designaciones = relationship('Designacion', secondary=categoria_designacion_table, back_populates='categorias')

    old_id = Column(String)

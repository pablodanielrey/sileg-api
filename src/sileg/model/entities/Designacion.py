from sqlalchemy import Column, String, Date, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from model_utils import Base

from .Cargo import Cargo
from .Lugar import Lugar
from .Usuario import Usuario

categoria_designacion_table = Table('categoria_designacion', Base.metadata,
    Column('designacion_id', String, ForeignKey('designacion.id')),
    Column('categoria_id', String, ForeignKey('categoria.id'))
)

class Designacion(Base):

    __tablename__ = 'designacion'

    desde = Column(Date)
    hasta = Column(Date)
    historico = Column(Boolean)

    expediente = Column(String)
    resolucion = Column(String)

    tipo = Column(String)
    categorias = relationship('Categoria', secondary=categoria_designacion_table, back_populates='designaciones')

    designacion_id = Column(String, ForeignKey('designacion.id'))
    designacion = relationship('Designacion', foreign_keys=[designacion_id])
    #designacion = relationship('Designacion', back_populates='designaciones')

    #designaciones = relationship('Designacion', back_populates='designacion')

    usuario_id = Column(String, ForeignKey('usuario.id'))
    usuario = relationship('Usuario', back_populates='designaciones')

    cargo_id = Column(String, ForeignKey('cargo.id'))
    cargo = relationship('Cargo', back_populates='designaciones')

    lugar_id = Column(String, ForeignKey('lugar.id'))
    lugar = relationship('Lugar', back_populates='designaciones')

    old_id = Column(String)

    _mapper_args__ = {
        'polymorphic_on':tipo,
        'polymorphic_identity':'designacion'
    }


    @classmethod
    def find(cls, session):
        query = session.query(cls).join(Designacion.usuario).join(Designacion.lugar).join(Designacion.cargo)
        return query


Usuario.designaciones = relationship('Designacion', back_populates='usuario')
Cargo.designaciones = relationship('Designacion', back_populates='cargo')
Lugar.designaciones = relationship('Designacion', back_populates='lugar')


class BajaDesignacion(Designacion):
    __mapper_args__ = {
        'polymorphic_identity':'baja'
    }


class Categoria(Base):

    __tablename__ = 'categoria'

    nombre = Column(String, unique=True)

    designaciones = relationship('Designacion', secondary=categoria_designacion_table, back_populates='categorias')

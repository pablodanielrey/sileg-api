from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from model_utils import Base

class Materia(Base):

    __tablename__ = 'materia'

    nombre = Column(String)
    old_id = Column(String)

    @classmethod
    def find(cls, session):
        return session.query(cls)

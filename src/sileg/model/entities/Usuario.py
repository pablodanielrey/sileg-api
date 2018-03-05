from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from model_utils import Base

#from .Designacion import Designacion

import json
import requests

class Usuario(Base):

    __tablename__ = 'usuario'

    designaciones = relationship('Designacion', back_populates='designacion')

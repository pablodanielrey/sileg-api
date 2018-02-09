from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from model_utils import Base

#from .Designacion import Designacion

import json
import requests

class Usuario(Base):

    __tablename__ = 'usuario'

    designaciones = relationship('Designacion', back_populates='designacion')

    def resolveUser(self):
        ''' se hace la llamada rest a la api de usuarios '''
        r = requests.get('http://usuarios.econo.unlp.edu.ar/users/api/v1.0/usuarios/{}'.format(self.id))
        if r.ok:
            return r.json()
        else:
            return None

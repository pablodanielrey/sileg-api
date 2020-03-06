from flask_wtf import FlaskForm
from wtforms import StringField

from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.Place import Place, PlaceTypes


class PlaceSearchForm(FlaskForm):
    query = StringField('Buscar lugar')
    class Meta:
        csrf = False        

    
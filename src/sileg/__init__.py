from flask import Flask
from .config import Config

"""
    Instancia de aplicacion
"""
app = Flask(__name__)
app.config.from_object(Config)

"""
    Sessiones
"""
###Sesiones
#from flask_session import Session
###Seteo de tipo de almacenamiento de sesion en el servidor
#app.config['SESSION_TYPE'] = 'filesystem'
#Session(app)

"""
    Registro de blueprints
"""
## Registro bueprint web base
from .bp.web.index import bp as bp_web_index
app.register_blueprint(bp_web_index)
## Registro bueprint personas
from .bp.web.persons import bp as bp_web_persons
app.register_blueprint(bp_web_persons,url_prefix='/personas')
## Registro bueprint web lugares
from .bp.web.places import bp as bp_web_places
app.register_blueprint(bp_web_places,url_prefix='/lugares')
## Registro bueprint web designaciones
from .bp.web.designations import bp as bp_web_designations
app.register_blueprint(bp_web_designations,url_prefix='/designaciones')
## Registro bueprint web licencias
from .bp.web.leavelicense import bp as bp_web_leavelicense
app.register_blueprint(bp_web_leavelicense,url_prefix='/licencias')
## Registro bueprint api ciudades
from .bp.rest.api.cities import bp as bp_api_cities
app.register_blueprint(bp_api_cities,url_prefix='/api/v0.1/ciudades')

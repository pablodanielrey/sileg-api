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
##BP
from .bp.web.index import bp as bp_web_index
app.register_blueprint(bp_web_index)
from .bp.web.users import bp as bp_web_users
app.register_blueprint(bp_web_users,url_prefix='/usuarios')
from .bp.web.places import bp as bp_web_places
app.register_blueprint(bp_web_places,url_prefix='/lugares')
from .bp.web.designations import bp as bp_web_designations
app.register_blueprint(bp_web_designations,url_prefix='/designaciones')


def main():
    app.run(host='0.0.0.0', port=10202, debug=False)

if __name__ == '__main__':
    main()
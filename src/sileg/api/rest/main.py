
import os
import logging
logging.getLogger().setLevel(logging.DEBUG)

from werkzeug.contrib.fixers import ProxyFix
from flask import Flask
from flask_cors import CORS

from rest_utils import register_encoder

app = Flask(__name__, static_url_path='/src/sileg/web')
app.wsgi_app = ProxyFix(app.wsgi_app)
register_encoder(app)
CORS(app)

from .converters import registrar
registrar(app)

OIDC_URL = os.environ['OIDC_URL']
DEBUGGING = bool(int(os.environ.get('VSC_DEBUGGING',0)))
def configurar_debugger():
    """
    para debuggear con visual studio code
    """
    if DEBUGGING:
        print('Iniciando Debugger PTVSD')
        import ptvsd
        #secret = os.environ.get('VSC_DEBUG_KEY',None)
        port = int(os.environ.get('VSC_DEBUGGING_PORT', 5678))
        ptvsd.enable_attach(address=('0.0.0.0',port))

configurar_debugger()

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'

    return r


"""
    registro los blueprints
"""
from . import gelis
app.register_blueprint(gelis.bp)
#app.register_blueprint(webpush.bp)
#app.register_blueprint(sileg.app)

def main():
    app.run(host='0.0.0.0', port=10202, debug=False)

if __name__ == '__main__':
    main()

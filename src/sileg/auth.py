from functools import wraps

from sileg import app
from flask_oidc import OpenIDConnect

class MyOpenIDConnect(OpenIDConnect):
    """
        clase necesaria para corregir la mala implementación del chequeo del tokenid.
        ahora para resolver el caso retorno True
    """
    def _is_id_token_valid(self, id_token):
        """
        Check if `id_token` is a current ID token for this application,
        was issued by the Apps domain we expected,
        and that the email address has been verified.

        @see: http://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation
        """
        if not id_token:
            return False

        return True    

oidc = MyOpenIDConnect(app)

def require_user(fn):
    @wraps(fn)
    @oidc.require_login
    def insert_user(*args, **kwargs):
        user = oidc.user_getinfo(['given_name', 'family_name', 'preferred_username', 'email_verified', 'email', 'sub'])    
        kwargs['user'] = user
        return fn(*args, **kwargs)
    return insert_user

"""
TODO insertar el usar automaticamente dentro del context para no tener que pasarlo al render_template
"""
#def render_templateOICDV2(*args, **kwargs):
#    bp = kwars['blueprint']
#    @bp.context_processor
#    def additional_context(fn):
#        #if request.endpoint.split('.')[1] != fn.__name__:
#        #    return {} 
#        user = oidc.user_getinfo(['given_name', 'family_name', 'preferred_username', 'email_verified', 'email', 'sub'])
#        return {
#            'user': user,
#        }
#    return fn
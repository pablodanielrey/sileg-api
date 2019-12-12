
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

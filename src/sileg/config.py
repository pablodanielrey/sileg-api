import os

class Config():
    """
        Clase para contener configs y obtener datos desde env
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'algo-asdasdasgdkjhgdfjkgbrj-loco'
    SILEG_DB_HOST = os.environ.get('SILEG_DB_HOST')
    SILEG_DB_NAME = os.environ.get('SILEG_DB_NAME')
    SILEG_DB_USER = os.environ.get('SILEG_DB_USER')
    SILEG_DB_PASSWORD = os.environ.get('SILEG_DB_PASSWORD')
    SILEG_DB_PORT = os.environ.get('SILEG_DB_PORT')

    OIDC_CLIENT_SECRETS = os.environ.get('OIDC_CLIENT_SECRETS')
    OIDC_COOKIE_SECURE = False
    OIDC_ID_TOKEN_COOKIE_SECURE = False
    OIDC_CLOCK_SKEW = 0
    OIDC_REQUIRE_VERIFIED_EMAIL = False
    #OIDC_INTROSPECTION_AUTH_METHOD = 'client_secret_basic'
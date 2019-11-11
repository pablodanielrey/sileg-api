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
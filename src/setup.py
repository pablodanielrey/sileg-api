"""
    https://packaging.python.org/distributing/
    https://pypi.python.org/pypi?%3Aaction=list_classifiers
    http://semver.org/

    zero or more dev releases (denoted with a ”.devN” suffix)
    zero or more alpha releases (denoted with a ”.aN” suffix)
    zero or more beta releases (denoted with a ”.bN” suffix)
    zero or more release candidates (denoted with a ”.rcN” suffix)
"""

from setuptools import find_packages, setup

setup(
    name="sileg-api",
    version="0.3.9",
    description="api del proyecto de las designaciones de docentes/no-docentes de la facultad",
    url="https://github.com/pablodanielrey/sileg-api",
    author="Desarrollo DiTeSi, FCE",
    author_email="ditesi@econo.unlp.edu.ar",
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=["contrib", "docs", "test*"]),
    install_requires=[
        "gunicorn",
        "requests",
        "Flask==1.1.2",
        "flask-wtf==0.14.3",
        "flask_jsontools==0.1.7",
        "flask-cors",
        "Flask-OIDC==1.4.0",
        "itsdangerous==1.1.0",
        "markupsafe==1.1.0",
        "WTForms==2.3.3",
        "Werkzeug==1.0.1",
        "SQLAlchemy==1.3.18",
        "SQLAlchemy-serializer==1.3.4.2",
        "psycopg2-binary==2.8.5",
        #'pulsar-client',
        "sileg-model",
        "users-model",
        "login-model"
        #'microservices_common>=2.0.7a1'
    ],
    entry_points={},
)

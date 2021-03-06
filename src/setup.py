"""
    https://packaging.python.org/distributing/
    https://pypi.python.org/pypi?%3Aaction=list_classifiers
    http://semver.org/

    zero or more dev releases (denoted with a ”.devN” suffix)
    zero or more alpha releases (denoted with a ”.aN” suffix)
    zero or more beta releases (denoted with a ”.bN” suffix)
    zero or more release candidates (denoted with a ”.rcN” suffix)
"""

from setuptools import setup, find_packages

setup(name='sileg-api',
          version='0.3.9',
          description='api del proyecto de las designaciones de docentes/no-docentes de la facultad',
          url='https://github.com/pablodanielrey/sileg-api',
          author='Desarrollo DiTeSi, FCE',
          author_email='ditesi@econo.unlp.edu.ar',
          classifiers=[
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6'
          ],
          packages=find_packages(exclude=['contrib', 'docs', 'test*']),
          install_requires=[
                            'gunicorn',
                            'requests',
                            'Flask',
                            'flask-wtf',
                            'flask_jsontools',
                            'flask-cors',
                            'Flask-OIDC',
                            'SQLAlchemy',
                            #'pulsar-client',
                            'sileg-model',
                            'users-model',
                            'login-model'
                            #'microservices_common>=2.0.7a1'
                          ],
          entry_points={
          }

      )

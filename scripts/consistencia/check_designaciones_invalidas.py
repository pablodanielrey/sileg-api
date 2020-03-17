
import sys
import psycopg2
import uuid
import json
import logging

from sileg_model.model import open_session
from sileg_model.model.SilegModel import SilegModel
from sileg_model.model.entities.Place import PlaceTypes, Place
from sileg_model.model.entities.Designation import Designation

from users.model.entities.User import User
from users.model.UsersModel import UsersModel
from users.model import open_session as open_user_session

#import ptvsd
#ptvsd.enable_attach(address = ('0.0.0.0', 10202))
#ptvsd.wait_for_attach()

silegModel = SilegModel()

def _obtener_arbol_de_lugares(session, lid, places=[]):
    """ genera dentro de places todos los ids de lugares del subarbol con raiz lid """
    if lid in places:
        return
    places.append(lid)
    ps = silegModel.get_places(session, [lid])
    if len(ps) <= 0:
        raise Exception('No se encuentra el lugar indicado')
    for p in ps[0].children:
        _obtener_arbol_de_lugares(session, p.id, places)

if __name__ == '__main__':

    with open_session() as session:

        pids = []
        _obtener_arbol_de_lugares(session, '06b1159e-8a83-4e4e-b8af-a8ad3dd47258', pids)
        dids = silegModel.get_designations_by_places(session, pids)
        designations = silegModel.get_designations(session, dids)
        total = len(designations)
        actual = 0
        with open_user_session() as usession:
            for d in designations:
                actual = actual + 1
                uid = d.user_id
                assert uid is not None
                try:
                    print(f"verificando {actual}/{total} : {uid}")
                    UsersModel.get_users(usession, [uid])
                except Exception as e:
                    logging.exception(e)
        
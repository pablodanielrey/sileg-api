import datetime

from sileg_model.model import open_session as open_sileg_session
from sileg_model.model.entities.Designation import Designation
from sileg_model.model.entities.Function import Function
from sileg_model.model.entities.Place import Place

from users.model import open_session as open_users_session
from users.model.entities.User import User



if __name__ == '__main__':

    users = []
    with open_users_session() as users:
        users = [u.id for u in users.query(User.id).all()]
    print(f"usuarios a chequear : {len(users)}")

    with open_sileg_session() as sileg:
        designations = [d for d in sileg.query(Designation.id, Designation.user_id).all()]
        print(f"designaciones a chequear {len(designations)}")
        for did, uid in designations:
            #if users.query(User.id).filter(User.id == uid).count() <= 0:
            if uid not in users:
                d = sileg.query(Designation).filter(Designation.id == did).one()
                d.deleted = datetime.datetime.utcnow()
                d.comments = 'NO EXISTE EL USUARIO'
                print(f'No existe el usuario {d.id} -- {uid}')
                sileg.commit()

            """
            pid = d.place_id
            if sileg.query(Place.id).filter(Place.id == pid).count() <= 0:
                d.deleted = datetime.datetime.utcnow()
                d.comments = 'NO EXITE EL LUGAR'
                print(f"no existe el lugar {d.id} -- {pid}")

            fid = d.function_id
            if sileg.query(Function.id).filter(Function.id == fid).count() <= 0:
                d.deleted = datetime.datetime.utcnow()
                d.comments = 'NO EXISTE LA FUCNIÓN'
                print(f"No existe la funcion {d.id} -- {fid}")
            """


if __name__ == '__main__':

    from sileg.model import obtener_session
    from sileg.model.entities import Cargo

    cargos = {
        # docentes

        Cargo(id='ca0c7105-ade2-4fab-b14c-086248b7a447', nombre='Titular D/S', tipo=Cargo._tipos[0]),
        Cargo(id='b65f8e8b-80ee-4ff8-9bf2-f04ba2bdd397', nombre='Adjunto D/S', tipo=Cargo._tipos[0]),
        Cargo(id='6f0c238b-808c-4692-ac26-aaccf3d22cb1', nombre='Asociado D/S', tipo=Cargo._tipos[0]),


        Cargo(id='99528020-6389-4d8e-a88d-5629b6b4cac0', nombre='Jefe de Trabajos Prácticos D/S', tipo=Cargo._tipos[0]),
        Cargo(id='dbf391cd-1212-4e40-a795-f466b0c2406d', nombre='Ayudante Diplomado D/S', tipo=Cargo._tipos[0]),
        Cargo(id='750780c1-496a-4ca9-bcb7-9b3835f205c1', nombre='Ayudante Alumno D/S', tipo=Cargo._tipos[0]),

        Cargo(id='718e8e33-2989-4337-8d79-2609268d315e', nombre='Jefe de Auxiliares Docentes D/S', tipo=Cargo._tipos[0]),
        Cargo(id='07bac038-f4a8-437b-843e-607ea89b72e2', nombre='Cumple Funciones', tipo=Cargo._tipos[0]),

        #autoridades

        Cargo(id='325e5e55-375b-4768-9e7b-c14de0a85553', nombre='Secretario', tipo=Cargo._tipos[2]),
        Cargo(id='84a2bc10-f82d-489b-962c-1a8f25bd1796', nombre='Pro Secretario', tipo=Cargo._tipos[2]),
        Cargo(id='28b3a978-15ad-4c17-9421-c1fd75ee01ef', nombre='Vicedecano', tipo=Cargo._tipos[2]),
        Cargo(id='06adf7ed-51a9-4774-8606-0f46a69fbadf', nombre='Decano', tipo=Cargo._tipos[2]),

        # no docentes

        Cargo(id='245eae51-28c4-4c6b-9085-354606399666', nombre='Cumple Funciones', tipo=Cargo._tipos[1])
    }


    with obtener_session() as s:
        for c in cargos:
            c1 = s.query(Cargo).filter(Cargo.id == c.id).one_or_none()
            if c1:
                c1.nombre = c.nombre
                c1.tipo = c.tipo
            else:
                s.add(c)
            s.commit()
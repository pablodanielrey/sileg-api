"""
utndocentes=> select * from tipo_dedicacion;
 tipodedicacion_id | tipodedicacion_nombre | tipodedicacion_factaextender | tipodedicacion_abrev | usuario_log 
-------------------+-----------------------+------------------------------+----------------------+-------------
                 3 | Exclusiva             | 0                            | D/E                  |            
                 2 | Semi Exclusiva        | 0                            | S/D                  |            
                 7 | Simple                | 1                            | D/S                  |            
                 8 | Tiempo completo       | 0                            | T.comp.              |           6
                 9 | Semidedicación        | 1                            | S/D                  |          40
                11 | A-H                   | 1                            | A-H                  |          40
                12 | ...                   | 0                            | .                    |          47

 desig_tipodedicacion_id | desig_tipocargo_id |            fullname             
-------------------------+--------------------+---------------------------------
                       2 |                  2 | Asociado S/D
                       3 |                  2 | Asociado D/E
                       7 |                  2 | Asociado D/S
                       2 |                  3 | Adjunto S/D
                       3 |                  3 | Adjunto D/E
                       7 |                  3 | Adjunto D/S
                       9 |                  3 | Adjunto S/D
                      11 |                  3 | Adjunto A-H
                      12 |                  3 | Adjunto .
                       2 |                  4 | Jefe de Auxiliares Docentes S/D
                       3 |                  4 | Jefe de Auxiliares Docentes D/E
                       7 |                  4 | Jefe de Auxiliares Docentes D/S
                       9 |                  4 | Jefe de Auxiliares Docentes S/D
                       2 |                  5 | Ayudante Diplomado S/D
                       3 |                  5 | Ayudante Diplomado D/E
                       7 |                  5 | Ayudante Diplomado D/S
                       9 |                  5 | Ayudante Diplomado S/D
                      11 |                  5 | Ayudante Diplomado A-H
                      12 |                  5 | Ayudante Diplomado .
                       7 |                  6 | Ayudante Alumno D/S
                       2 |                  9 | Titular S/D
                       3 |                  9 | Titular D/E
                       7 |                  9 | Titular D/S
                       9 |                  9 | Titular S/D
                      11 |                  9 | Titular A-H
                       3 |                 16 | Decano D/E
                       3 |                 17 | Vicedecano D/E
                       7 |                 17 | Vicedecano D/S
                       3 |                 18 | Secretario D/E
                       7 |                 18 | Secretario D/S
                       8 |                 18 | Secretario T.comp.
                      11 |                 18 | Secretario A-H
                       3 |                 20 | Prosecretario D/E
                       8 |                 20 | Prosecretario T.comp.
                       3 |                 21 | ... D/E
                      11 |                 21 | ... A-H
                      12 |                 21 | ... .
"""


if __name__ == '__main__':

    from sileg.model import obtener_session
    from sileg.model.entities import Cargo

    cargos = {
        # docentes
        Cargo(id='ca0c7105-ade2-4fab-b14c-086248b7a447', nombre='Titular D/S', tipo=Cargo._tipos[0], old_id='c9d7'),
        Cargo(id='015d50a9-b3db-4119-b20d-a931ee377e8b', nombre='Titular S/E', tipo=Cargo._tipos[0], old_id='c9d2'),
        Cargo(id='b3901ac4-7fc8-43b5-85d7-34da6728bc21', nombre='Titular D/E', tipo=Cargo._tipos[0], old_id='c9d3'),
        Cargo(id='3a75074b-f98e-46ba-9f66-11d15f566abf', nombre='Titular S/D', tipo=Cargo._tipos[0], old_id='c9d9'),
        Cargo(id='708673ce-1092-4419-af45-514effc8a604', nombre='Titular A-H', tipo=Cargo._tipos[0], old_id='c9d11'),
        
        Cargo(id='6f0c238b-808c-4692-ac26-aaccf3d22cb1', nombre='Asociado D/S', tipo=Cargo._tipos[0], old_id='c2d7'),
        Cargo(id='6341dd1e-d57e-4378-a9fa-c7a6cc66f336', nombre='Asociado S/E', tipo=Cargo._tipos[0], old_id='c2d2'),
        Cargo(id='eeceeac9-12c1-479f-a8eb-a88aa19d286c', nombre='Asociado D/E', tipo=Cargo._tipos[0], old_id='c2d3'),

        Cargo(id='b65f8e8b-80ee-4ff8-9bf2-f04ba2bdd397', nombre='Adjunto D/S', tipo=Cargo._tipos[0], old_id=''),
        
        Cargo(id='99528020-6389-4d8e-a88d-5629b6b4cac0', nombre='Jefe de Trabajos Prácticos D/S', tipo=Cargo._tipos[0], old_id=''),
        Cargo(id='dbf391cd-1212-4e40-a795-f466b0c2406d', nombre='Ayudante Diplomado D/S', tipo=Cargo._tipos[0], old_id=''),
        Cargo(id='750780c1-496a-4ca9-bcb7-9b3835f205c1', nombre='Ayudante Alumno D/S', tipo=Cargo._tipos[0], old_id=''),

        Cargo(id='718e8e33-2989-4337-8d79-2609268d315e', nombre='Jefe de Auxiliares Docentes D/S', tipo=Cargo._tipos[0], old_id=''),
        Cargo(id='07bac038-f4a8-437b-843e-607ea89b72e2', nombre='Cumple Funciones', tipo=Cargo._tipos[0], old_id=None),

        #autoridades

        Cargo(id='325e5e55-375b-4768-9e7b-c14de0a85553', nombre='Secretario', tipo=Cargo._tipos[2], old_id=''),
        Cargo(id='84a2bc10-f82d-489b-962c-1a8f25bd1796', nombre='Pro Secretario', tipo=Cargo._tipos[2], old_id=''),
        Cargo(id='28b3a978-15ad-4c17-9421-c1fd75ee01ef', nombre='Vicedecano', tipo=Cargo._tipos[2], old_id=''),
        Cargo(id='06adf7ed-51a9-4774-8606-0f46a69fbadf', nombre='Decano', tipo=Cargo._tipos[2], old_id='c16d3'),

        # no docentes

        Cargo(id='245eae51-28c4-4c6b-9085-354606399666', nombre='Cumple Funciones', tipo=Cargo._tipos[1], old_id=None)
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
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
import logging
logging.getLogger().setLevel(logging.DEBUG)


if __name__ == '__main__':

    from sileg.model import obtener_session
    from sileg.model.entities import Cargo

    cargos = {
        
        # docentes
        Cargo(id='04c938ea-b4b7-4ef2-8c19-6b8d254d1539', nombre='Beca (D)', tipo=Cargo._tipos[0], old_id=None),
        Cargo(id='2228918a-3802-4683-8add-f27274ed5beb', nombre='Contrato (D)', tipo=Cargo._tipos[0], old_id=None),
        Cargo(id='07bac038-f4a8-437b-843e-607ea89b72e2', nombre='Cumple Funciones (D)', tipo=Cargo._tipos[0], old_id=None),

        Cargo(id='ca0c7105-ade2-4fab-b14c-086248b7a447', nombre='Titular D/S', tipo=Cargo._tipos[0], old_id='c9d7'),
        Cargo(id='015d50a9-b3db-4119-b20d-a931ee377e8b', nombre='Titular D/SE', tipo=Cargo._tipos[0], old_id='c9d2'),
        Cargo(id='b3901ac4-7fc8-43b5-85d7-34da6728bc21', nombre='Titular D/E', tipo=Cargo._tipos[0], old_id='c9d3'),
        Cargo(id='3a75074b-f98e-46ba-9f66-11d15f566abf', nombre='Titular S/D', tipo=Cargo._tipos[0], old_id='c9d9'),
        Cargo(id='708673ce-1092-4419-af45-514effc8a604', nombre='Titular A-H', tipo=Cargo._tipos[0], old_id='c9d11'),
        
        Cargo(id='6f0c238b-808c-4692-ac26-aaccf3d22cb1', nombre='Asociado D/S', tipo=Cargo._tipos[0], old_id='c2d7'),
        Cargo(id='6341dd1e-d57e-4378-a9fa-c7a6cc66f336', nombre='Asociado D/SE', tipo=Cargo._tipos[0], old_id='c2d2'),
        Cargo(id='eeceeac9-12c1-479f-a8eb-a88aa19d286c', nombre='Asociado D/E', tipo=Cargo._tipos[0], old_id='c2d3'),

        Cargo(id='b65f8e8b-80ee-4ff8-9bf2-f04ba2bdd397', nombre='Adjunto D/S', tipo=Cargo._tipos[0], old_id='c3d7'),
        Cargo(id='d1a0e4a7-03ca-40a9-a98c-d89cdc322d9a', nombre='Adjunto D/SE', tipo=Cargo._tipos[0], old_id='c3d2'),
        Cargo(id='8349f5fa-c988-41d4-9ac4-14609448f4ce', nombre='Adjunto D/E', tipo=Cargo._tipos[0], old_id='c3d3'),
        Cargo(id='ffdf4a49-253f-4e64-94af-8a033e3a9992', nombre='Adjunto S/D', tipo=Cargo._tipos[0], old_id='c3d9'),
        Cargo(id='a398549b-20d0-4d47-a500-7daf353eaa54', nombre='Adjunto A-H', tipo=Cargo._tipos[0], old_id='c3d11'),        
        
        Cargo(id='5fa3f450-f379-41b8-9b34-26b5e14edc3f', nombre='Jefe de Trabajos Prácticos D/SE', tipo=Cargo._tipos[0], old_id='c4d2'),
        Cargo(id='4680eeea-e534-4515-91d0-e7b456397b68', nombre='Jefe de Trabajos Prácticos D/E', tipo=Cargo._tipos[0], old_id='c4d3'),
        Cargo(id='99528020-6389-4d8e-a88d-5629b6b4cac0', nombre='Jefe de Trabajos Prácticos D/S', tipo=Cargo._tipos[0], old_id='c4d7'),
        Cargo(id='5c0de1de-4c4a-46bf-b0e5-3582bb280404', nombre='Jefe de Trabajos Prácticos S/D', tipo=Cargo._tipos[0], old_id='c4d9'),

        Cargo(id='dbf391cd-1212-4e40-a795-f466b0c2406d', nombre='Ayudante Diplomado D/S', tipo=Cargo._tipos[0], old_id='c5d7'),
        Cargo(id='37df5825-6640-4568-965e-4478b49e9868', nombre='Ayudante Diplomado D/SE', tipo=Cargo._tipos[0], old_id='c5d2'),
        Cargo(id='b4c0d4b6-923f-4f55-8b0a-053e5864e525', nombre='Ayudante Diplomado D/E', tipo=Cargo._tipos[0], old_id='c5d3'),
        Cargo(id='2266437a-6055-4a2c-9242-2e36f4429bfd', nombre='Ayudante Diplomado S/D', tipo=Cargo._tipos[0], old_id='c5d9'),
        Cargo(id='a45eb272-0a35-4571-ae32-853b1ec1ec29', nombre='Ayudante Diplomado A-H', tipo=Cargo._tipos[0], old_id='c5d11'),

        Cargo(id='750780c1-496a-4ca9-bcb7-9b3835f205c1', nombre='Ayudante Alumno D/S', tipo=Cargo._tipos[0], old_id='c6d7'),

        
        #Auxiliares Docentes es lo mismo que Jefe de Trabajos Prácticos
        #Cargo(id='718e8e33-2989-4337-8d79-2609268d315e', nombre='Jefe de Auxiliares Docentes D/S', tipo=Cargo._tipos[0], old_id=''),

        #autoridades
        Cargo(id='06adf7ed-51a9-4774-8606-0f46a69fbadf', nombre='Decano', tipo=Cargo._tipos[2], old_id='c16d3'),

        Cargo(id='28b3a978-15ad-4c17-9421-c1fd75ee01ef', nombre='Vicedecano D/E', tipo=Cargo._tipos[2], old_id='c17d3'), 
        Cargo(id='ebe588ed-baa7-4499-9858-ccd7c0fdf8be', nombre='Vicedecano D/S', tipo=Cargo._tipos[2], old_id='c17d7'), 

        Cargo(id='325e5e55-375b-4768-9e7b-c14de0a85553', nombre='Secretario D/E', tipo=Cargo._tipos[2], old_id='c18d3'),
        Cargo(id='315ddd75-25ae-46f1-a506-1e61457dd906', nombre='Secretario D/S', tipo=Cargo._tipos[2], old_id='c18d7'),
        Cargo(id='b1068227-2ab8-41c1-8e90-68c6a53911c2', nombre='Secretario D/C', tipo=Cargo._tipos[2], old_id='c18d8'),
        Cargo(id='bfebbbcf-523b-4c40-9306-7527a224479f', nombre='Secretario A-H', tipo=Cargo._tipos[2], old_id='c18d11'),

        Cargo(id='84a2bc10-f82d-489b-962c-1a8f25bd1796', nombre='Pro Secretario D/E', tipo=Cargo._tipos[2], old_id='c20d3'),
        Cargo(id='39dac568-b5e5-495d-a445-0bda5beac073', nombre='Pro Secretario D/C', tipo=Cargo._tipos[2], old_id='c20d8'),

        # no docentes

        Cargo(id='245eae51-28c4-4c6b-9085-354606399666', nombre='Cumple Funciones (ND)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='c8a0afbc-3f52-474e-9e90-8163f6064ae8', nombre='Beca (ND)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='83338329-e5e5-4789-be8c-9216e8c2f319', nombre='Contrato (ND)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='17f6f48e-4121-498f-ae1f-36ea72ad437e', nombre='A01', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='085009b4-fb68-44be-85f3-9f572e4b111b', nombre='A02', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='7f34ebda-988f-4a52-a394-f9ee107b5258', nombre='A03', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='90951706-cfe4-45ab-8984-a7ff93cef4f1', nombre='A04', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='43d79ec0-94c6-4b5f-b63d-1ca890fd0f81', nombre='A05', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='b60be4d0-c687-4a9a-874b-47ab531560f9', nombre='A06', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='a81db9a2-13d5-4d99-bdc0-272c4c1dad6e', nombre='A07', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='2fc098e6-8511-4f17-af6f-cd39b272b1ca', nombre='B01', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='f5e0c5dc-12aa-4f62-9964-a7719ccd70f7', nombre='B02', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='71267199-d666-40d3-8038-9dad4ee31ce6', nombre='B03', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='796c4d5a-e7a3-4e32-bf8b-15f06b65d4ff', nombre='B04', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='81943f24-8162-4448-977e-ed9612a900b4', nombre='B05', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='c6c3ed9e-5d7a-4107-a585-04dd82c15b4b', nombre='B06', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='159fa8af-33dd-4ed8-b612-37bfbf77f5ba', nombre='B07', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='309bf902-930d-45c7-8a09-f01549273591', nombre='C01', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='1c1d5f05-f901-40d8-803d-0e0a19b807fa', nombre='C02', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='1e3ff867-566c-4396-b527-86c6afdbcab8', nombre='C03', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='522bd33e-db9d-423f-aced-ac2665ccb447', nombre='C04', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='da7817b0-aa97-4ac6-a2f7-8fe6dcd3178b', nombre='C05', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='ee99c697-96d7-404d-91e2-06379e1bd85e', nombre='C06', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='d9cf0d97-72f9-45ec-9343-b03dff103af3', nombre='C07', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='7835372e-bc8a-43f5-9516-51db6c7623ee', nombre='D01', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='c72fec13-fc0a-4490-a064-4d699927d0d4', nombre='D02', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='a9fb7e1d-14ba-4a3e-933d-877d25f0f19b', nombre='D03', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='f7cc46bf-fac9-42c6-a601-6b4bd53f771e', nombre='D04', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='92376384-8fff-4275-a63a-3eb729f3c686', nombre='D05', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='68a03e60-6559-4059-b614-d9a67441688b', nombre='D06', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='a70f25f5-42b2-42fd-8f45-d0aad99371e3', nombre='D07', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='ed2944f0-465f-4d7c-9978-3d29d16017ba', nombre='E01', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='edcf53a3-40b1-4ba1-b572-77daf3b913ab', nombre='E02', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='aad34f62-948a-499c-a071-c3027612c9d0', nombre='E03', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='12d2ea0d-abf9-42e4-82b8-4603188c0e01', nombre='E04', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='a6bdc2a9-82c0-42a3-abb9-e43566b1f468', nombre='E05', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='7a506ef0-f4ce-40bc-ab1d-8f400c83ec8f', nombre='E06', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='8ca9db52-c079-44b9-b66c-a629a586afae', nombre='E07', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='43d47a78-e2f3-4686-b96f-594720d0ea4a', nombre='Cumple Funciones (A01)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='77012394-e855-44ba-a2e3-9ff81680f86e', nombre='Cumple Funciones (A02)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='2394685e-e83a-40fd-b096-18b8535f3043', nombre='Cumple Funciones (A03)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='cca357de-81ea-4295-a095-3c498a92d2ce', nombre='Cumple Funciones (A04)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='de1361f5-f2e6-4fd1-be21-be05cf0fe7e3', nombre='Cumple Funciones (A05)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='0dbe5670-78e9-4291-b7ca-85aed65027ab', nombre='Cumple Funciones (A06)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='381e6b28-895c-43af-a0c3-67fde16e93f8', nombre='Cumple Funciones (A07)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='d76d2117-7d9a-4213-b088-cfda1322f847', nombre='Cumple Funciones (B01)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='390284aa-b8cb-4d59-9e73-b1e14e5f8dfd', nombre='Cumple Funciones (B02)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='ae292b4e-cc1c-41fc-82fd-f0795cc49c04', nombre='Cumple Funciones (B03)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='882d9330-0fe3-4dbb-9d18-4740ea833e9a', nombre='Cumple Funciones (B04)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='294d272e-8327-4f62-b89a-878de98aa7b1', nombre='Cumple Funciones (B05)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='3652605e-5523-46a2-a5b1-69d967e0bd88', nombre='Cumple Funciones (B06)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='33253ca0-9ac1-4dcd-b662-d503fbb28379', nombre='Cumple Funciones (B07)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='10f604a2-83dd-4432-9d39-d549ef1ad646', nombre='Cumple Funciones (C01)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='567d0c22-acef-424a-9224-2c1797a33a54', nombre='Cumple Funciones (C02)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='db1c0615-c32c-4448-90b7-01760d3fc24c', nombre='Cumple Funciones (C03)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='999ac482-d5f1-443c-bfaf-92465b63245e', nombre='Cumple Funciones (C04)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='6a0ff748-a59f-4ed7-a78b-ca4dff1fe138', nombre='Cumple Funciones (C05)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='9a7a2fa8-7790-4f8f-b571-305a7675d528', nombre='Cumple Funciones (C06)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='69ef9445-5bd6-4b52-a436-1d41ed92e019', nombre='Cumple Funciones (C07)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='845c426d-f785-4e35-b6ad-be530c742f43', nombre='Cumple Funciones (D01)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='5763dcb0-ac73-427d-8056-8e4ddf67a8b3', nombre='Cumple Funciones (D02)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='89b98b17-d4f1-4140-96d8-dddfb9154b29', nombre='Cumple Funciones (D03)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='c0b6d95a-48d3-4333-9fa0-27f36027c47e', nombre='Cumple Funciones (D04)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='9f4ea01a-155f-41b3-a4d2-dd83743b2e96', nombre='Cumple Funciones (D05)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='edad509b-8fa0-4891-a5df-569b675b13c0', nombre='Cumple Funciones (D06)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='3bd0724a-2e22-4a31-a6a4-3babfe6c73ca', nombre='Cumple Funciones (D07)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='c6481f48-026f-432d-86ee-e461a52ab1f4', nombre='Cumple Funciones (E01)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='71a40daa-da44-4348-aed4-f6669920c570', nombre='Cumple Funciones (E02)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='04b846a0-e609-4fa0-97f4-b248799ef3f4', nombre='Cumple Funciones (E03)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='6806a862-10eb-4673-ac23-ced264212295', nombre='Cumple Funciones (E04)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='ab314cd8-9b33-41d1-adf5-69a53ef72851', nombre='Cumple Funciones (E05)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='0fe4a1f3-3ace-4cd2-9ecd-fe4af1d33a94', nombre='Cumple Funciones (E06)', tipo=Cargo._tipos[1], old_id=None),
        Cargo(id='7ac85f03-94b1-47ce-a30d-dc964eedc7fb', nombre='Cumple Funciones (E07)', tipo=Cargo._tipos[1], old_id=None),
        
        # alumnos

        Cargo(id='74913809-2c2e-4ece-9546-5da8148adc71', nombre='Alumno Proyecto', tipo=Cargo._tipos[4], old_id=None)
    }


    with obtener_session() as s:
        for c in cargos:
            c1 = s.query(Cargo).filter(Cargo.id == c.id).one_or_none()
            if c1:
                logging.info("Actualizando cargo {}".format(c.nombre))
                c1.nombre = c.nombre
                c1.tipo = c.tipo
            else:
                logging.info("Creando cargo {}".format(c.nombre))
                s.add(c)
            s.commit()
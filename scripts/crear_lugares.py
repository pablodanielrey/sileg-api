

def crear_lugares(s, padre_id, lugares):
    for l in lugares:
        logging.debug('procesando {}'.format(l['lugar'].nombre))
        c = s.query(Lugar).filter(Lugar.id == l['lugar'].id).one_or_none()
        if c:
            logging.debug('actualizando {}'.format(l['lugar'].nombre))
            c.nombre = l['lugar'].nombre
            c.padre_id = padre_id
        else:
            logging.debug('creando {}'.format(l['lugar'].nombre))
            s.add(l['lugar'])
        s.commit()
        if 'hijos' in l and len('hijos') > 0:
            crear_lugares(s, l['lugar'].id, l['hijos'])


def imprimir_lugar(s, tabs, l):
    print('{} {} {}'.format(tabs, l.id, l.nombre))
    tabs2 = tabs + '    '
    for l1 in l.hijos:
        imprimir_lugar(s, tabs2, l1)


if __name__ == '__main__':

    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

    from sqlalchemy import or_
    from sileg.model import obtener_session
    from sileg.model.entities import Lugar, Facultad, Direccion, Departamento, Division, Secretaria


    """ muestro la estructura actual de lugares """

    """
    pid = None
    with obtener_session() as s:
        q = s.query(Lugar).filter(or_(Lugar.padre_id == None, Lugar.padre_id == '')).all()
        for l in q:
            imprimir_lugar(s, '', l)
    """


    """ creo los lugares """

    lugares = [
        {'lugar': Lugar(id='5776a70e-a9af-466d-b9c4-89e646fc39af', nombre='Desconocido')},
        {
            'lugar': Facultad(id='06b1159e-8a83-4e4e-b8af-a8ad3dd47258', nombre='Facultad de Ciencias Económicas (FCE)'),
            'hijos': [
                {
                    'lugar': Lugar(id='2d14c2ce-7a8c-45dc-8aab-3eeff0f2aa2c', nombre='NODOCENTE'),
                    'hijos': [
                        {'lugar': Secretaria(id='f450f268-ff9d-4e37-9628-0f4a9ed81a34', nombre='Secretaría de Administración y Finanzas')},
                        {
                            'lugar': Secretaria(id='387af5e1-f281-4aba-9454-1d5cbbb1f5c7', nombre='Secretaría Administrativa'),
                            'hijos':[
                                {'lugar': Division(id='2ec05fd9-7db9-4626-94c9-b682af530736', nombre='Limpieza')},
                                {'lugar': Direccion(id='6b74d542-bdca-432e-9840-a57ea5388e88', nombre='Dirección Docentes')},
                                {
                                    'lugar': Direccion(id='f788cdf9-d54e-46b7-a0a1-126110f1d843', nombre='Dirección de Biblioteca'),
                                    'hijos':[
                                        {'lugar': Departamento(id='1b04a0e3-502b-4c2e-9d7a-48c63c0af036', nombre='Departamento de Hemeroteca')},
                                        {'lugar': Departamento(id='8a84affe-8715-4e39-ba01-6ee93994d9f6', nombre='Departamento de Ciculación y Préstamos')}
                                    ]
                                },
                                {
                                    'lugar': Direccion(id='3e16756e-98f4-4e49-b047-1ea305dd7730', nombre='Dirección Económico Financiero'),
                                    'hijos':[
                                        {'lugar': Departamento(id='c113d920-c481-44ce-ad7b-971a7775cd44', nombre='Departamento de Compras')},
                                        {'lugar': Departamento(id='6d57e17f-f582-4fd2-8056-6c2bd53b264a', nombre='Departamento de Tesorería')},
                                        {'lugar': Departamento(id='69206b65-69b8-4fc8-910f-bd85f308f27f', nombre='Departamento de Registros Contables')},
                                        {'lugar': Division(id='606ef94f-993e-4526-958f-8573d9b4df2d', nombre='División de Inventario')}
                                    ]
                                },
                                {
                                    'lugar': Direccion(id='8407abb2-33c2-46e7-bef6-d00bab573306', nombre='Mantenimiento y Servicios Generales'),
                                    'hijos':[
                                        {'lugar': Division(id='0b3a7cae-9c12-44b5-b1d8-bbf680911d53', nombre='Mantenimiento')},
                                        {'lugar': Division(id='90630d44-9c79-4742-91c2-4219baa02f7f', nombre='Servicios Generales')}
                                    ]
                                },
                                {
                                    'lugar': Direccion(id='4e82fbed-9b4e-4707-a9ac-9246d85b5d49', nombre='Dirección de Enseñanza'),
                                    'hijos':[
                                        {'lugar': Departamento(id='f4a5de0c-8168-446b-b01d-dfe8f2f88abd', nombre='Departamento de Alumnos')}
                                    ]
                                },
                                {'lugar': Division(id='1b65fe02-a5c7-431e-8226-517fb275c4a2', nombre='Impresiones')},
                                {
                                    'lugar': Direccion(id='5986c50e-52f9-4a96-8d91-602bbcf1cd61', nombre='Dirección del Área Operativa'),
                                    'hijos':[
                                        {'lugar': Departamento(id='fe736967-e618-4766-8bf0-b7bdf22ce922', nombre='Departamento de Mesa de Entradas')},
                                        {'lugar': Departamento(id='988e2b23-2fd7-497e-974a-4a0a25b85744', nombre='Departamento de Personal')},
                                        {'lugar': Departamento(id='8ed6353f-3f33-4747-9db1-f60609f52601', nombre='Departamento de Despacho')},
                                        {'lugar': Departamento(id='a07fbca6-d068-4bfb-94d7-9699d864d4c3', nombre='Departamento de Consejo Académico')},
                                        {'lugar': Departamento(id='eb761eb4-42f6-4925-af11-bbabad85f388', nombre='Departamento de Concursos')}
                                    ]
                                },
                                {'lugar': Direccion(id='b13c1ce9-65f9-42fb-93c7-2556b63eb058', nombre='Dirección de Tecnologías y Sistemas Informática (DiTeSI)')},
                                {'lugar': Direccion(id='7bf4ba90-aa92-44e1-a111-dfad7890b70b', nombre='Dirección de Doctorado y Posgrado')}
                            ]
                        }
                    ]
                }
            ]
        }
    ]


    personas = [
        {
            # finanzas
            'lid':'f450f268-ff9d-4e37-9628-0f4a9ed81a34',
            'dnis':['27947761', '28390126', '31256282']
        },
        {
            # administrativa
            'lid': '4f677488-3eca-4f53-ba36-e50d2c2640ac',
            'dnis': ['27528150', '27528195', '32393755', '34770399']
        }
    ]


    with obtener_session() as s:
        crear_lugares(s, None, lugares)
        s.commit()
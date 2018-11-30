

def crear_lugares(s, padre_id, lugares):
    for l in lugares:
        c = s.query(Lugar).filter(Lugar.id == l['lugar'].id).one_or_none()
        if c:
            c.nombre = l['lugar'].nombre
        else:
            s.add(l['lugar'])


def imprimir_lugar(s, tabs, l):
    print('{} {} {}'.format(tabs, l.id, l.nombre))
    tabs2 = tabs + '    '
    for l1 in l.hijos:
        imprimir_lugar(s, tabs2, l1)


if __name__ == '__main__':

    import logging
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

    from sqlalchemy import or_
    from sileg.model import obtener_session
    from sileg.model.entities import Lugar, Facultad


    """ muestro la estructura actual de lugares """

    pid = None
    with obtener_session() as s:
        q = s.query(Lugar).filter(or_(Lugar.padre_id == None, Lugar.padre_id == '')).all()
        for l in q:
            imprimir_lugar(s, '', l)


    """ creo los lugares """

    lugares = [{
        'lugar': Facultad(id='67bb4146-46aa-4602-b019-6ea189dbb779', nombre='Facultad de Ciencias Económicas (FCE)'),
        'hijos': [{
            'lugar': Facultad(id='f450f268-ff9d-4e37-9628-0f4a9ed81a34', nombre='Secretaría de Administración y Finanzas'),
            'hijos': [{
                'lugar': Facultad(id='4f677488-3eca-4f53-ba36-e50d2c2640ac', nombre='Secretaría Administrativa'),
                'hijos':[{
                    'lugar': Facultad(id='f788cdf9-d54e-46b7-a0a1-126110f1d843', nombre='Dirección de Biblioteca'),
                    'hijos':[
                        {'lugar': Facultad(id='', nombre='Departamento de Hemeroteca')},
                        {'lugar': Facultad(id='', nombre='Departamento de Ciculación y Préstamos')}
                    ]},
                    {'lugar': Facultad(id='', nombre='Dirección Económico Financiero'),
                    'hijos':[
                        {'lugar': Facultad(id='', nombre='Departamento de Compras')},
                        {'lugar': Facultad(id='', nombre='Departamento de Tesorería')},
                        {'lugar': Facultad(id='', nombre='Departamento de Registros Contables')}
                    ]},
                    {'lugar': Facultad(id='8407abb2-33c2-46e7-bef6-d00bab573306', nombre='Dirección de Mantenimiento y Servicios Generales'),
                    'hijos':[
                        {'lugar': Facultad(id='', nombre='Mantenimiento')},
                        {'lugar': Facultad(id='', nombre='Servicios Generales')}
                    ]},
                    {'lugar': Facultad(id='', nombre='Dirección de Enseñanza'),
                    'hijos':[
                        {'lugar': Facultad(id='', nombre='Departamento de Alumnos')},
                        {'lugar': Facultad(id='', nombre='Sala de Profesores')}
                    ]},
                    {'lugar': Facultad(id='', nombre='Impresiones')},
                    {'lugar': Facultad(id='', nombre='Dirección del Área Operativa'),
                    'hijos':[
                        {'lugar': Facultad(id='', nombre='Departamento de Mesa de Entradas')},
                        {'lugar': Facultad(id='', nombre='Departamento de Personal')},
                        {'lugar': Facultad(id='', nombre='Departamento de Despacho')},
                        {'lugar': Facultad(id='', nombre='Departamento de Consejo Académico')},
                        {'lugar': Facultad(id='', nombre='Departamento de Concursos')}
                    ]},
                    {'lugar': Facultad(id='', nombre='Dirección de Tecnologías y Sistemas Informática')},
                    {'lugar': Facultad(id='', nombre='Dirección de Doctorado y Posgrado')}
                }]
            }]
        }]
    }]

    pid = None
    with obtener_session() as s:
        for c in lugares:
            crear_lugares(s, pid, [c])
            if len(c['hijos']) > 0:
                pid = c['lugar'].id
                crear_lugares(s, pid, c['hijos'])
            s.commit()
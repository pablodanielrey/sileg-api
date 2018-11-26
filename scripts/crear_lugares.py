

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

    """
    lugares = [{
        'lugar': Facultad(id='67bb4146-46aa-4602-b019-6ea189dbb779', nombre='Facultad de Ciencias Económicas (FCE)'),
        'hijos': []
    }]

    pid = None
    with obtener_session() as s:
        for c in lugares:
            crear_lugares(s, pid, [c])
            if len(c['hijos']) > 0:
                pid = c['lugar'].id
                crear_lugares(s, pid, c['hijos'])
            s.commit()
    """
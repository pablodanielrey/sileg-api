
import uuid

with open('c.txt','w') as f:
    for c in ['A','B','C','D','E']:
        for n in range(1,8):
            cid = uuid.uuid4()
            car = '{}0{}'.format(c,n) 
            f.write("Cargo(id='{}', nombre='{}', tipo=Cargo._tipos[1], old_id=None),\n".format(cid,car))

    for c in ['A','B','C','D','E']:
        for n in range(1,8):
            cid = uuid.uuid4()
            car = '{}0{}'.format(c,n) 
            f.write("Cargo(id='{}', nombre='Cumple Funciones ({})', tipo=Cargo._tipos[1], old_id=None),\n".format(cid,car))
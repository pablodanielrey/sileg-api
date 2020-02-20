from users.model.entities.User import IdentityNumberTypes, DegreeTypes

"""
Manejador de traducciones de nombres para la interfaz
"""

def id2sIdentityNumber(id:IdentityNumberTypes):
    if id == IdentityNumberTypes.DNI:
        return 'DNI'
    if id == IdentityNumberTypes.LC:
        return 'LC'
    if id == IdentityNumberTypes.LE:
        return 'LE'
    if id == IdentityNumberTypes.PASSPORT:
        return 'Pasaporte'
    if id == IdentityNumberTypes.CUIL:
        return 'CUIL'
    if id == IdentityNumberTypes.CUIT:
        return 'CUIT'
    return ''    

def id2sDegrees(id:DegreeTypes):
    if id == DegreeTypes.ELEMENTARY:
        return 'Primario'
    if id == DegreeTypes.HIGHER:
        return 'Secundario'
    if id == DegreeTypes.COLLEGE:
        return 'Grado'
    if id == DegreeTypes.MASTER:
        return 'Maestría'
    if id == DegreeTypes.DOCTORAL:
        return 'Doctorado'
    return ''
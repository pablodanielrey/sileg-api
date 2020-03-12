from functools import wraps

def verify_user_permissions(fn):
    @wraps(fn)
    def verify_permission(*args, **kwargs):
        user = kwargs['user']
        uid = user['sub']

        nuestros_uids = {
            '27294557':'89d88b81-fbc0-48fa-badb-d32854d3d93a',
            '34928857':'3ca3057b-adba-49b3-8b99-550311fc9c81',
            '34770038':'13b2471b-507e-44d7-a440-efdb66d5aaa8'
        }

        if uid in nuestros_uids.values():
            return fn(*args, **kwargs)
        else:
            raise Exception('no permitido')
    return verify_permission

def verify_students_permission(fn):
    @wraps(fn)
    def verify_permission(*args, **kwargs):
        user = kwargs['user']
        uid = user['sub']

        nuestros_uids = {
            '27294557':'89d88b81-fbc0-48fa-badb-d32854d3d93a',
            '34928857':'3ca3057b-adba-49b3-8b99-550311fc9c81',
            '34770038':'13b2471b-507e-44d7-a440-efdb66d5aaa8',
            '26106655':'4719252a-ef58-4522-a776-d497708d2812'
        }

        if uid in nuestros_uids.values():
            return fn(*args, **kwargs)
        else:
            raise Exception('no permitido')
    return verify_permission 

def verify_sileg_permission(fn):
    @wraps(fn)
    def verify_permission(*args, **kwargs):
        user = kwargs['user']
        uid = user['sub']

        nuestros_uids = {
            '27294557':'89d88b81-fbc0-48fa-badb-d32854d3d93a',
            '34928857':'3ca3057b-adba-49b3-8b99-550311fc9c81',
            '34770038':'13b2471b-507e-44d7-a440-efdb66d5aaa8'
        }

        if uid in nuestros_uids.values():
            return fn(*args, **kwargs)
        else:
            raise Exception('no permitido')
    return verify_permission 

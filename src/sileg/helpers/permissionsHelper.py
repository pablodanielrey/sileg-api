from functools import wraps

def verify_admin_permissions(fn):
    @wraps(fn)
    def verify_permission(*args, **kwargs):
        user = kwargs['user']
        uid = user['sub']

        nuestros_uids = {
            '27294557':'89d88b81-fbc0-48fa-badb-d32854d3d93a',
            '34928857':'3ca3057b-adba-49b3-8b99-550311fc9c81',
            '34770038':'13b2471b-507e-44d7-a440-efdb66d5aaa8',
            '29694757':'35f7a8a6-d844-4d6f-b60b-aab810610809',
            '31073351':'d44e92c1-d277-4a45-81dc-a72a76f6ef8d',
            '30001823':'205de802-2a15-4652-8fde-f23c674a1246'            
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
            '26106655':'4719252a-ef58-4522-a776-d497708d2812',
            '27528150':'853cd3dd-739c-4423-a88e-4fe722209fc7',
            '27528195':'af2ba1fb-66ce-4857-b226-1b19b1d3a0c5',
            '32393755':'15022185-5e14-4772-a620-53fadf843bc0',
            '30001823':'205de802-2a15-4652-8fde-f23c674a1246'
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
            '34770038':'13b2471b-507e-44d7-a440-efdb66d5aaa8',
            '29694757':'35f7a8a6-d844-4d6f-b60b-aab810610809',
            '31073351':'d44e92c1-d277-4a45-81dc-a72a76f6ef8d',
            '27528150':'853cd3dd-739c-4423-a88e-4fe722209fc7',
            '27528195':'af2ba1fb-66ce-4857-b226-1b19b1d3a0c5',
            '32393755':'15022185-5e14-4772-a620-53fadf843bc0',
            '26106655':'4719252a-ef58-4522-a776-d497708d2812',
            '30001823':'205de802-2a15-4652-8fde-f23c674a1246'
        }

        if uid in nuestros_uids.values():
            return fn(*args, **kwargs)
        else:
            raise Exception('no permitido')
    return verify_permission 

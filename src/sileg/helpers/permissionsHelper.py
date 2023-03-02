from functools import wraps


def verify_admin_permissions(fn):
    @wraps(fn)
    def verify_permission(*args, **kwargs):
        user = kwargs["user"]
        uid = user["sub"]

        nuestros_uids = {
            "27294557": "89d88b81-fbc0-48fa-badb-d32854d3d93a",  # Pablo
            "34928857": "3ca3057b-adba-49b3-8b99-550311fc9c81",  # Migue
            "34770038": "13b2471b-507e-44d7-a440-efdb66d5aaa8",  # Leo
            "29694757": "35f7a8a6-d844-4d6f-b60b-aab810610809",  # Jano
            "31073351": "d44e92c1-d277-4a45-81dc-a72a76f6ef8d",  # Ivan
            "30001823": "205de802-2a15-4652-8fde-f23c674a1246",  # Walter
            "33221190": "4eb89203-7f1e-4558-9d2d-6a037f6ff9b4",  # Maripaz
            "26106655": "4719252a-ef58-4522-a776-d497708d2812",  # Emilio,
        }

        if uid in nuestros_uids.values():
            return fn(*args, **kwargs)
        else:
            raise Exception("no permitido")

    return verify_permission


def verify_sileg_permission(fn):
    @wraps(fn)
    def verify_permission(*args, **kwargs):
        user = kwargs["user"]
        uid = user["sub"]

        nuestros_uids = {
            "27294557": "89d88b81-fbc0-48fa-badb-d32854d3d93a",  # Pablo
            "34928857": "3ca3057b-adba-49b3-8b99-550311fc9c81",  # Migue
            "34770038": "13b2471b-507e-44d7-a440-efdb66d5aaa8",  # Leo
            "29694757": "35f7a8a6-d844-4d6f-b60b-aab810610809",  # Jano
            "31073351": "d44e92c1-d277-4a45-81dc-a72a76f6ef8d",  # Ivan
            "30001823": "205de802-2a15-4652-8fde-f23c674a1246",  # Walter
            "33221190": "4eb89203-7f1e-4558-9d2d-6a037f6ff9b4",  # Maripaz
            "27528150": "853cd3dd-739c-4423-a88e-4fe722209fc7",  # Julio
            "27528195": "af2ba1fb-66ce-4857-b226-1b19b1d3a0c5",  # Silvina
            "32393755": "15022185-5e14-4772-a620-53fadf843bc0",  # Pablo Lozada
            "22851309": "2fa4895a-a5b0-43da-81eb-c8bd7c034609",  # Sara Cuervo - a pedido de Pablo Lozada
            "26106655": "4719252a-ef58-4522-a776-d497708d2812",  # Emilio
        }

        if uid in nuestros_uids.values():
            return fn(*args, **kwargs)
        else:
            raise Exception("no permitido")

    return verify_permission


def verify_students_permission(fn):
    @wraps(fn)
    def verify_permission(*args, **kwargs):
        user = kwargs["user"]
        uid = user["sub"]

        nuestros_uids = {
            "27294557": "89d88b81-fbc0-48fa-badb-d32854d3d93a",  # Pablo
            "34928857": "3ca3057b-adba-49b3-8b99-550311fc9c81",  # Migue
            "34770038": "13b2471b-507e-44d7-a440-efdb66d5aaa8",  # Leo
            "29694757": "35f7a8a6-d844-4d6f-b60b-aab810610809",  # Jano
            "31073351": "d44e92c1-d277-4a45-81dc-a72a76f6ef8d",  # Ivan
            "30001823": "205de802-2a15-4652-8fde-f23c674a1246",  # Walter
            "33221190": "4eb89203-7f1e-4558-9d2d-6a037f6ff9b4",  # Maripaz
            "27528150": "853cd3dd-739c-4423-a88e-4fe722209fc7",  # Julio
            "27528195": "af2ba1fb-66ce-4857-b226-1b19b1d3a0c5",  # Silvina
            "32393755": "15022185-5e14-4772-a620-53fadf843bc0",  # Pablo Lozada
            "22851309": "2fa4895a-a5b0-43da-81eb-c8bd7c034609",  # Sara Cuervo - a pedido de Pablo Lozada
            "26106655": "4719252a-ef58-4522-a776-d497708d2812",  # Emilio
            "40998560": "723c901b-f52e-4c4b-a8ba-944a12e19439",  # Agustin tactagi - a pedido de emilio
            "43317682": "c51d34c7-08a1-4458-9a5b-3fdf15f016bb",  # paloma timossi - a pedido de emilio
        }

        if uid in nuestros_uids.values():
            return fn(*args, **kwargs)
        else:
            raise Exception("no permitido")

    return verify_permission

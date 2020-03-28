
from users.model.UsersModel import UsersModel
import users.model
from users.model.entities.User import IdentityNumberTypes, MailTypes

usersModel = UsersModel
open_users_session = users.model.open_session

def _get_institutional_mails(user):
    return [m for m in user.mails if m.type is MailTypes.INSTITUTIONAL and m.deleted == None]


from sileg_model.model.SilegModel import SilegModel
import sileg_model.model

silegModel = SilegModel()
open_sileg_session = sileg_model.model.open_session

from login.model import obtener_session as open_login_session
from login.model.LoginModel import LoginModel
loginModel = LoginModel()

from .EventsModel import EventsModel
eventsModel = EventsModel()


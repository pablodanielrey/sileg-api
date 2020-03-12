
from users.model.UsersModel import UsersModel
import users.model
from users.model.entities.User import IdentityNumberTypes

from sileg_model.model.SilegModel import SilegModel
import sileg_model.model

usersModel = UsersModel
open_users_session = users.model.open_session

silegModel = SilegModel()
open_sileg_session = sileg_model.model.open_session

from login.model import obtener_session as open_login_session
from login.model.LoginModel import LoginModel
loginModel = LoginModel()
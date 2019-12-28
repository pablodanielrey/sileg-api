
from users.model.UsersModel import UsersModel
import users.model

from sileg_model.model.SilegModel import SilegModel
import sileg_model.model

usersModel = UsersModel
open_users_session = users.model.open_session

silegModel = SilegModel()
open_sileg_session = sileg_model.model.open_session

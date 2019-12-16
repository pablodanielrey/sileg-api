
from users.model.UsersModel import UsersModel
from users.model.entities import Usuario
import users.model

usersModel = UsersModel
userEntity = Usuario

open_users_session = users.model.open_session


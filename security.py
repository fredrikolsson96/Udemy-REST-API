from models.user import UserModel
from werkzeug.security import safe_str_cmp

# authenticate user on username & password
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# get user from the request's JSON payload 
def identity(payload):
    user_id = payload.get('identity')
    return UserModel.find_by_id(user_id)
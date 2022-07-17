from models.user import UserModel

# function to authenticate to a user
def authenticate(username,password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload): # this function is unique to Flask-JWT
    # payload is the contents of the JWT token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

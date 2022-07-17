from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required=True,
        help = 'This field cannot be blank'
    )
    parser.add_argument('password',
        type = str,
        required=True,
        help = 'This field cannot be blank'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        # checking if user already exists or not
        if UserModel.find_by_username(data['username']) is not None:
            # user exists
            return {'message' : 'A user with that user name already exists'} , 400 # for bad request

        # user does not exist
        user = UserModel(data['username'] , data['password'])
        user.save_to_db()
        return {'message' : 'User created succesfully'} , 201 # 201 for created
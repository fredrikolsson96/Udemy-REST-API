import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field cannot be blank'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field cannot be blank'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        # check if a user with that username already exists
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        user = UserModel(**data)
        try:
            # save the user to the database
            user.save_to_db()
        except:
            return {'An error occurred while saving to the database'}, 500

        return {'message': 'User created successfully'}, 201
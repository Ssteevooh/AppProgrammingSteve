from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.user import User
from schemas.user import UserSchema

# TODO UserListResource

user_schema = UserSchema()


class UserResource(Resource):

    #@jwt_required
    def get(self, username):

        user = User.get_by_username(username=username)

        current_user = get_jwt_identity()

       #if current_user is None:
            #return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN


        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        return user_schema.dump(user), HTTPStatus.OK

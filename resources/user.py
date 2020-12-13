from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.user import User
from schemas.user import UserSchema

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class UserListResource(Resource):

    @jwt_required
    def get(self):

        current_user = get_jwt_identity()

        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        users = User.get_all()

        return user_list_schema.dump(users).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        # Only for admins
        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user), HTTPStatus.CREATED


class UserResource(Resource):

    @jwt_required
    def get(self, username):

        user = User.get_by_username(username=username)

        current_user = get_jwt_identity()

        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        return user_schema.dump(user), HTTPStatus.OK

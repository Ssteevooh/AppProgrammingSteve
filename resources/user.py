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

        current_user = get_jwt_identity()

        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)
        if errors:
            return {"message": "Validation errors", "errors":  errors}, HTTPStatus.BAD_REQUEST

        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        if User.get_by_username(data.get("username")):
            return {"message": "Username already exists."}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user), HTTPStatus.CREATED


class UserResource(Resource):

    @jwt_required
    def get(self, user_id):

        user = User.get_by_id(user_id=user_id)

        current_user = get_jwt_identity()

        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        return user_schema.dump(user), HTTPStatus.OK

    @jwt_required
    def patch(self, user_id):

        json_data = request.get_json()
        current_user = get_jwt_identity()

        user = User.get_by_id(user_id=user_id)

        if current_user is None and user.role > 1:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        data, errors = user_schema.load(data=json_data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        user.user_id = user.user_id
        user.role = data.get("role") or user.role
        user.username = data.get("username") or user.username
        user.password = data.get("password") or user.password
        user.is_active = data.get("is_active") or user.is_active
        user.created_at = user.created_at
        user.updated_at = user.updated_at
        user.save()

        return {'message': 'Updated'}, HTTPStatus.OK

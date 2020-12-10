from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.storage import Storage
from schemas.storage import StorageSchema

# NOTE
# user roles:
# 0 = client
# 1 =  merchant
# 2 = admin

storage_schema = StorageSchema()
storage_list_schema = StorageSchema(many=True)


class StorageListResource(Resource):

    @jwt_required
    def get(self):

        current_user = get_jwt_identity()

        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        storages = Storage.get_all()

        return storage_list_schema.dump(storages).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        # Only for admins
        if current_user is None or current_user.role < 2:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        data, errors = storage_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        storage = Storage(**data)
        storage.save()

        return storage_schema.dump(storage).data, HTTPStatus.CREATED


class StorageResource(Resource):

    @jwt_required
    def get(self, storage_id):

        current_user = get_jwt_identity()

        # For every role
        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        storage = Storage.get_by_id(storge_id=storage_id)

        if storage is None:
            return {'message': 'Storage not found'}, HTTPStatus.NOT_FOUND

        return storage_schema.dump(storage).data, HTTPStatus.OK

    @jwt_required
    def patch(self, storage_id):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        if current_user.role < 1:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        data, errors = storage_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        storage = Storage.get_by_id(storage_id=storage_id)

        if storage is None:
            return {'message': 'Storage not found'}, HTTPStatus.NOT_FOUND

        storage.place = data.get('place') or storage.place
        storage.size = data.get('size') or storage.size
        storage.description = data.get('description') or storage.description

        storage.save()

        return storage_schema.dump(storage).data, HTTPStatus.OK

    @jwt_required
    def delete(self, storage_id):

        current_user = get_jwt_identity()

        # Only for  admins
        if current_user.role != 2:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        storage = Storage.get_by_id(storage_id=storage_id)

        if storage is None:
            return {'message': 'Storage not found'}, HTTPStatus.NOT_FOUND

        storage.delete()

        return {}, HTTPStatus.NO_CONTENT

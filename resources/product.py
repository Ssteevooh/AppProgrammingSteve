from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.product import Product


# TODO ProductListResource


class ProductResource(Resource):

    @jwt_required
    def get(self, product_id):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        if current_user is None:
            return {'message': 'Unauthorized!'}, HTTPStatus.UNAUTHORIZED

        product = Product.get_by_id(product_id=product_id)

        if product is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return json_data, HTTPStatus.OK

    @jwt_required
    def patch(self, product_id):

        json_data = request.get_json()

        product = Product.get_by_id(product_id=product_id)

        if product is None:
            return {'message': 'Product not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user.role < 1:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        product.name = json_data.get('name') or product.name
        product.description = json_data.get('description') or product.description
        product.stock = json_data.get('num_of_servings') or product.stock
        product.price = json_data.get('cook_time') or product.price
        product.size = json_data.get('ingredients') or product.size

        product.save()

        return json_data, HTTPStatus.OK

    @jwt_required
    def delete(self, product_id):

        product = Product.get_by_id(product_id=product_id)

        if product is None:
            return {'message': 'Product not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user.role != 2:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        product.delete()

        return {}, HTTPStatus.NO_CONTENT

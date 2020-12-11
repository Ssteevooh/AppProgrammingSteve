from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from models.product import Product
from schemas.product import ProductSchema

# NOTE
# user roles:
# 0 = client
# 1 =  merchant
# 2 = admin

# TODO implement patch visibilities for roles ie client can decrement stock

product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)


class ProductListResource(Resource):

    @jwt_required
    def get(self):

        current_user = get_jwt_identity()

        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        products = Product.get_all()

        return product_list_schema.dump(products), HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        #Only for admins
        if current_user is None or current_user.role < 2:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        data, errors = product_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        product = Product(**data)
        product.save()

        return product_schema.dump(product), HTTPStatus.CREATED


class ProductResource(Resource):

    #@jwt_required
    def get(self, product_id):

        current_user = get_jwt_identity()

        #For every role
        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        product = Product.get_by_id(product_id=product_id)

        if product is None:
            return {'message': 'Product not found'}, HTTPStatus.NOT_FOUND

        return product_schema.dump(product), HTTPStatus.OK

    @jwt_required
    def patch(self, product_id):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        # TODO implement patch visibilities for roles ie client can decrement stock
        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        data, errors = product_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        product = Product.get_by_id(product_id=product_id)

        if product is None:
            return {'message': 'Product not found'}, HTTPStatus.NOT_FOUND

        product.id = data.get("product_id") or product.product_id
        product.name = data.get("product_name") or product.name
        product.description = data.get("description") or product.description
        product.steps = data.get("stock") or product.steps
        product.tools = data.get("price") or product.tools
        product.cost = data.get("size") or product.cost
        #product.updated_at = data.get("updated_at")

        product.save()

        return product_schema.dump(product), HTTPStatus.OK

    @jwt_required
    def delete(self, product_id):

        current_user = get_jwt_identity()

        # Only for  admins
        if current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        product = Product.get_by_id(product_id=product_id)

        if product is None:
            return {'message': 'Product not found'}, HTTPStatus.NOT_FOUND

        product.delete()

        return {}, HTTPStatus.NO_CONTENT

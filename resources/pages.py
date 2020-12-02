from http import HTTPStatus
from flask import render_template, make_response
from flask_restful import Resource


class LoginResource(Resource):

    def get(self):
        return make_response(render_template("login.html"), HTTPStatus.OK)


class OrderResource(Resource):
    def get(self):
        return make_response(render_template("order.html"), HTTPStatus.OK)


class ConfirmResource(Resource):
    def get(self):
        return make_response(render_template("confirm.html"), HTTPStatus.OK)

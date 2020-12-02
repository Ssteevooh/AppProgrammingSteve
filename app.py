from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt

from resources.token import TokenResource, RefreshResource, RevokeResource
from resources.pages import LoginResource, OrderResource, ConfirmResource
from resources.product import ProductResource, ProductListResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)

    api.add_resource(TokenResource, "/token")
    api.add_resource(RefreshResource, "/refresh")
    api.add_resource(RevokeResource, "/revoke")

    api.add_resource(LoginResource, "/")
    api.add_resource(OrderResource, "/order")
    api.add_resource(ConfirmResource, "/confirm")

    api.add_resource(ProductResource, "/product/<int:product_id>")
    api.add_resource(ProductListResource, "/products")


if __name__ == "__main__":
    app = create_app()
    app.run()

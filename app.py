from flask import Flask, render_template
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt

from resources.product import ProductResource


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    register_extensions(app)
    register_resources(app)

    return app

def register_extensions(app):
    db.init_app(app)
    # migrate = Migrate(app, db)
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)

    api.add_resource(ProductResource, "/product/<int:product_id>")


if __name__ == "__main__":
    app = create_app()
    app.run()

# @app.route("/login", methods=["GET"])
# def login():
#    return render_template("login.html")


# @app.route("/order", methods=["GET"])
# def order():
#    return render_template("order.html")


# @app.route("/confirm", methods=["GET"])
# def confirm():
#    return render_template("Confirm.html")
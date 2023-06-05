from flask import Flask
from .blueprints.oee import oee


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    app.register_blueprint(oee)

    return app

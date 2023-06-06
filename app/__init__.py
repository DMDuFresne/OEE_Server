from flask import Flask
from .blueprints.oee import oee
from .limiter import limiter


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    limiter.init_app(app)

    app.register_blueprint(oee)

    return app

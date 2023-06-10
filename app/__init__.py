from flask import Flask
from .limiter import limiter
from .database import db
from config import DevelopmentConfig
from .blueprints.oee import oee_blueprint
from .blueprints.historian import historian_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    limiter.init_app(app)

    app.register_blueprint(oee_blueprint, url_prefix='/oee')
    app.register_blueprint(historian_blueprint, url_prefix='/historian')  # Register the historian blueprint

    return app

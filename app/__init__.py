from flask import Flask
from .limiter import limiter
from .database import db
from config import DevelopmentConfig
from .blueprints.asset import asset_blueprint
from .blueprints.oee import oee_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    limiter.init_app(app)

    app.register_blueprint(asset_blueprint, url_prefix='/asset')
    app.register_blueprint(oee_blueprint, url_prefix='/oee')

    return app

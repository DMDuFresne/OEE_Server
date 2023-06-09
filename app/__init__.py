from flask import Flask
from .limiter import limiter
from .database import db
from config import DevelopmentConfig
from .blueprints.oee import oee_blueprint
from .blueprints.db import db_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(db_blueprint, url_prefix='/db')
    app.register_blueprint(oee_blueprint, url_prefix='/oee')

    return app
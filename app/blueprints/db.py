import config
from flask import Blueprint, request, jsonify
from app.services.db import set_db_config, validate_db_connection
from app.limiter import limiter


db_blueprint = Blueprint('db', __name__)


@db_blueprint.route('/config', methods=['POST'])
@limiter.limit("60/minute")
def set_db_config_route():
    data = request.get_json()
    # data.get('url'), data.get('username'), data.get('password')
    response, status = set_db_config(data)
    return jsonify(response), status


@db_blueprint.route('/validate', methods=['GET'])
@limiter.limit("60/minute")
def validate_db_connection_route():
    try:

        if hasattr(config, 'SQLALCHEMY_DATABASE_URI'):

            db_uri = config.SQLALCHEMY_DATABASE_URI
            if validate_db_connection(db_uri):

                return jsonify({'message': 'Database connection successful'}), 200

            else:

                return jsonify({'error': 'Database connection failed'}), 500

        else:

            return jsonify({'error': 'Database configuration not set'}), 400

    except Exception as e:

        return jsonify({'error': str(e)}), 500



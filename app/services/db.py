import os
import json
import config
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def save_db_config():
    config_data = {"SQLALCHEMY_DATABASE_URI": config.SQLALCHEMY_DATABASE_URI}
    with open('db_config.json', 'w') as f:
        json.dump(config_data, f)


def load_db_config():
    if os.path.exists('db_config.json'):
        with open('db_config.json', 'r') as f:
            config_data = json.load(f)
        config.SQLALCHEMY_DATABASE_URI = config_data.get('SQLALCHEMY_DATABASE_URI')


def set_db_config(data):
    try:

        # Check if all parameters are provided
        if 'address' not in data:
            raise ValueError('Missing address parameter')
        if 'database' not in data:
            raise ValueError('Missing database parameter')
        if 'username' not in data:
            raise ValueError('Missing username parameter')
        if 'password' not in data:
            raise ValueError('Missing password parameter')

        # Extract the parameters from the data
        db_address = data.get('address')
        db_database = data.get('database')
        db_username = data.get('username')
        db_password = data.get('password')

        # Construct the SQLAlchemy connection string
        conn_string = f"postgresql://{db_username}:{db_password}@{db_address}/{db_database}"

        if validate_db_connection(conn_string):
            # Store this connection string in your configuration
            config.SQLALCHEMY_DATABASE_URI = conn_string

            # Save the DB config
            save_db_config()

            return {'message': 'Database configuration updated'}, 200
        else:
            return {'message': 'Database configuration has not been updated - Connection is Invalid'}, 200

    except Exception as e:
        # Handle any other error
        return {'error': str(e)}, 500


def validate_db_connection(db_uri):
    engine = create_engine(db_uri)

    try:
        # Try to connect to the database
        connection = engine.connect()

    except OperationalError as oe:
        # The database connection failed
        raise ValueError("Database connection failed. Please check the database URI and try again.")

    except Exception as e:
        # An unexpected error occurred
        raise Exception("An unexpected error occurred while trying to connect to the database.")

    else:
        # The database connection was successful
        connection.close()
        return True


load_db_config()


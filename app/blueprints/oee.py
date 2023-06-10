# Import necessary modules
from flask import Blueprint, request
from app.services.oee import calculate_oee
from app.services.historian import insert_oee_data
from app.limiter import limiter

# Create a Flask blueprint for OEE calculations
oee_blueprint = Blueprint('oee', __name__)

# Define the routes for OEE


@oee_blueprint.route('/calculate', methods=['POST'])
@limiter.limit("60/minute")
def calculate():
    data = request.get_json()
    result = calculate_oee(data)
    return result


@oee_blueprint.route('/calculate_and_log', methods=['POST'])
@limiter.limit("60/minute")
def calculate_and_log():
    data = request.get_json()
    result = calculate_oee(data)

    # Insert the calculated OEE data into the database
    insert_response, insert_status = insert_oee_data(result)

    # Check if the insert was successful
    if insert_status != 200:
        # If there was an error, return the error response
        return insert_response, insert_status

    # If the insert was successful, return the OEE calculation result
    return result, 200


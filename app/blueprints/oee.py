# Import necessary modules
from flask import Blueprint, request, jsonify
from app.services.oee import calculate_oee, get_latest_oee, get_oee_by_date_range
from app.services.historian import insert_oee_data
from app.limiter import limiter
import logging

# Create a Flask blueprint for OEE calculations
oee_blueprint = Blueprint('oee', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define the routes for OEE


@oee_blueprint.route('/calculate', methods=['POST'])
@limiter.limit("60/minute")
def calculate_route():
    data = request.get_json()
    result = calculate_oee(data)
    return result


@oee_blueprint.route('/calculate/store', methods=['POST'])
@limiter.limit("60/minute")
def calculate_and_store_route():
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


@oee_blueprint.route('/<int:object_type>/<int:object_id>', methods=['GET'])
@limiter.limit("60/minute")
def get_latest_oee_route(object_type, object_id):
    # Retrieve OEE data from the historian based on the object_type and object_id
    oee_data = get_latest_oee(object_type, object_id)

    # Check if OEE data is found
    if oee_data is None:
        return jsonify({'error': 'OEE data not found for the specified object'}), 404

    return jsonify(oee_data), 200


@oee_blueprint.route('/history/<int:object_type>/<int:object_id>', methods=['GET'])
@limiter.limit("60/minute")
def get_oee_by_date_range_route(object_type, object_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({'error': 'start_date and end_date parameters are required.'}), 400

    try:
        # Call the service to get OEE data by date range
        oee_data = get_oee_by_date_range(object_type, object_id, start_date, end_date)
        return jsonify(oee_data), 200

    except Exception as e:
        logger.error(f"An error occurred while fetching OEE data by date range: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while fetching OEE data by date range.'}), 500


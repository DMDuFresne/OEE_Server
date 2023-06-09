# Import necessary modules
from flask import Blueprint, request
from app.services.oee import calculate_oee
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

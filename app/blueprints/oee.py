# Import necessary modules
from flask import Blueprint, request
from app.services.oee import calculate_oee

# Create a Flask blueprint for OEE calculations
oee = Blueprint('oee', __name__)

# Define the routes for OEE


@oee.route('/oee/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    result = calculate_oee(data)
    return result

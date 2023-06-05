from flask import Blueprint, request
from app.services.oee import calculate_oee

oee = Blueprint('oee', __name__)


@oee.route('/oee/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    result = calculate_oee(data)
    return result

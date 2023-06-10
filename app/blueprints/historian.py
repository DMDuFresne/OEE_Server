from flask import Blueprint, request
from app.services.historian import insert_oee_data
from app.limiter import limiter

historian_blueprint = Blueprint('historian', __name__)


@historian_blueprint.route('/insert', methods=['POST'])
@limiter.limit("60/minute")
def insert():
    data = request.get_json()
    insert_oee_data(data)
    return {"message": "Data inserted successfully"}, 200

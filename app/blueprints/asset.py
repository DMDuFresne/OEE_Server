from flask import Blueprint, request
from app.services.asset import *
from app.limiter import limiter

asset_blueprint = Blueprint('asset', __name__)


@asset_blueprint.route('/enterprise/create', methods=['POST'])
@limiter.limit("60/minute")
def route_create_enterprise():
    data = request.get_json()
    result = create_enterprise(data)
    return result


@asset_blueprint.route('/enterprise/all', methods=['GET'])
@limiter.limit("60/minute")
def route_get_all_enterprises():
    result = get_all_enterprises()
    return result


@asset_blueprint.route('/enterprise/<int:asset_id>', methods=['GET'])
@limiter.limit("60/minute")
def route_get_enterprise(asset_id):
    result = get_enterprise(asset_id)
    return result


@asset_blueprint.route('/enterprise/<int:asset_id>', methods=['PUT'])
@limiter.limit("60/minute")
def route_update_enterprise(asset_id):
    data = request.get_json()
    result = update_enterprise(data, asset_id)
    return result


@asset_blueprint.route('/enterprise/<int:asset_id>', methods=['DELETE'])
@limiter.limit("60/minute")
def route_delete_enterprise(asset_id):
    result = delete_enterprise(asset_id)
    return result


@asset_blueprint.route('/site/create', methods=['POST'])
@limiter.limit("60/minute")
def route_create_site():
    data = request.get_json()
    result = create_site(data)
    return result


@asset_blueprint.route('/site/all', methods=['GET'])
@limiter.limit("60/minute")
def route_get_all_sites():
    result = get_all_sites()
    return result


@asset_blueprint.route('/site/<int:asset_id>', methods=['GET'])
@limiter.limit("60/minute")
def route_get_site(asset_id):
    result = get_site(asset_id)
    return result


@asset_blueprint.route('/site/<int:asset_id>', methods=['PUT'])
@limiter.limit("60/minute")
def route_update_site(asset_id):
    data = request.get_json()
    result = update_site(data, asset_id)
    return result


@asset_blueprint.route('/site/<int:asset_id>', methods=['DELETE'])
@limiter.limit("60/minute")
def route_delete_site(asset_id):
    result = delete_site(asset_id)
    return result


@asset_blueprint.route('/area/create', methods=['POST'])
@limiter.limit("60/minute")
def route_create_area():
    data = request.get_json()
    result = create_area(data)
    return result


@asset_blueprint.route('/area/all', methods=['GET'])
@limiter.limit("60/minute")
def route_get_all_areas():
    result = get_all_areas()
    return result


@asset_blueprint.route('/area/<int:asset_id>', methods=['GET'])
@limiter.limit("60/minute")
def route_get_area(asset_id):
    result = get_area(asset_id)
    return result


@asset_blueprint.route('/area/<int:asset_id>', methods=['PUT'])
@limiter.limit("60/minute")
def route_update_area(asset_id):
    data = request.get_json()
    result = update_area(data, asset_id)
    return result


@asset_blueprint.route('/area/<int:asset_id>', methods=['DELETE'])
@limiter.limit("60/minute")
def route_delete_area(asset_id):
    result = delete_area(asset_id)
    return result

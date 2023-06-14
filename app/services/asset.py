from flask import jsonify
from app.models.asset import EnterpriseModel, SiteModel, AreaModel


def create_enterprise(data):

    try:
        asset = EnterpriseModel(**data)
        asset.create()
        if asset:
            return jsonify(asset.__dict__), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_all_enterprises():
    try:
        enterprises = EnterpriseModel.get_all()
        serialized = [enterprise.__dict__ for enterprise in enterprises]
        return jsonify(serialized), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_enterprise(asset_id):
    try:
        asset = EnterpriseModel().get(asset_id)
        if asset:
            return jsonify(asset.__dict__), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def update_enterprise(data, asset_id):
    try:
        asset = EnterpriseModel(**data)
        asset.update(asset_id)
        return jsonify(asset.__dict__), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_enterprise(asset_id):
    try:
        asset = EnterpriseModel().get(asset_id)
        if asset:
            asset.delete()
            return jsonify({
                'asset': asset.__dict__,
                'message': 'Enterprise deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Sites
# ----------
def create_site(data):

    try:
        asset = SiteModel(**data)
        asset.create()
        if asset:
            return jsonify(asset.__dict__), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_all_sites():
    try:
        sites = SiteModel.get_all()
        serialized = [site.__dict__ for site in sites]
        return jsonify(serialized), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_site(asset_id):
    try:
        asset = SiteModel().get(asset_id)
        if asset:
            return jsonify(asset.__dict__), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def update_site(data, asset_id):
    try:
        asset = SiteModel(**data)
        asset.update(asset_id)
        return jsonify(asset.__dict__), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_site(asset_id):
    try:
        asset = SiteModel().get(asset_id)
        if asset:
            asset.delete()
            return jsonify({
                'asset': asset.__dict__,
                'message': 'Site deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Areas
# ----------
def create_area(data):

    try:
        asset = AreaModel(**data)
        asset.create()
        if asset:
            return jsonify(asset.__dict__), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_all_areas():
    try:
        areas = AreaModel.get_all()
        serialized = [area.__dict__ for area in areas]
        return jsonify(serialized), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_area(asset_id):
    try:
        asset = AreaModel().get(asset_id)
        if asset:
            return jsonify(asset.__dict__), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def update_area(data, asset_id):
    try:
        asset = AreaModel(**data)
        asset.update(asset_id)
        return jsonify(asset.__dict__), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_area(asset_id):
    try:
        asset = AreaModel().get(asset_id)
        if asset:
            asset.delete()
            return jsonify({
                'asset': asset.__dict__,
                'message': 'Area deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

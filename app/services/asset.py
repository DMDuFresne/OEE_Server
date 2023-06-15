from flask import jsonify
from app.models.asset import *
# ^ This needs to stay - the models are passed from the route blueprint, and will fail without the import here.


def create_asset(asset_class, data):
    try:
        asset = asset_class(**data)
        asset.create()
        if asset:
            return jsonify(asset.__dict__), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_all_assets(asset_class):
    try:
        asset_instance = asset_class()
        assets = asset_instance.get_all()
        serialized = [asset.__dict__ for asset in assets]
        return jsonify(serialized), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_asset(asset_class, asset_id):
    try:
        asset = asset_class().get(asset_id)
        if asset:
            return jsonify(asset.__dict__), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def update_asset(asset_class, data, asset_id):
    try:
        asset = asset_class(**data)
        asset.update(asset_id)
        return jsonify(asset.__dict__), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_asset(asset_class, asset_id):
    try:
        asset = asset_class().get(asset_id)
        if asset:
            asset.delete()
            return jsonify({
                'asset': asset.__dict__,
                'message': f'{asset_class.__name__} deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

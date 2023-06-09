from flask import jsonify
from app.models.asset import *
from app.models.asset_tree import AssetTreeModel


logger = logging.getLogger(__name__)


def create_asset(asset_class, data):
    try:
        required_fields = ['name', 'description', 'parent_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        asset = asset_class(**data)
        asset.create()
        if asset:
            return jsonify({
                'data': asset.__dict__,
                'message': f'{asset_class.object_name} created successfully'
            }), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        logger.error(f"Error occurred while creating asset: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while creating the asset.'}), 500


def get_all_assets(asset_class):
    try:
        asset_instance = asset_class()
        assets = asset_instance.get_all()
        serialized = [asset.__dict__ for asset in assets]
        return jsonify({
            'data': serialized,
            'message': f'All {asset_class.object_name}s retrieved successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error occurred while fetching all assets: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while fetching all assets.'}), 500


def get_parent_asset(asset_class, asset_id):
    try:
        asset = asset_class()

        if asset.parent_table_name is None:
            return jsonify({'error': f'{asset.object_name}s have no parent.'}), 500

        assets = asset.get_parent(asset_id)
        serialized = [asset.__dict__ for asset in assets]
        return jsonify({
            'data': serialized,
            'message': f'the parent of the {asset_class.object_name} retrieved successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error occurred while fetching the parent asset: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while fetching the parent asset.'}), 500


def get_child_assets(asset_class, asset_id):
    try:
        asset = asset_class()

        if asset.child_table_name is None:
            return jsonify({'error': f'{asset.object_name}s have no children.'}), 500

        assets = asset.get_children(asset_id)
        serialized = [asset.__dict__ for asset in assets]
        return jsonify({
            'data': serialized,
            'message': f'Children of {asset_class.object_name}s retrieved successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error occurred while fetching child assets: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while fetching child assets.'}), 500


def get_asset(asset_class, asset_id):
    try:
        asset = asset_class().get(asset_id)
        if asset:
            return jsonify({
                'data': asset.__dict__,
                'message': f'{asset_class.object_name} retrieved successfully'
            }), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        logger.error(f"Error occurred while fetching asset: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while fetching the asset.'}), 500


def update_asset(asset_class, data, asset_id):
    try:
        asset = asset_class(**data)
        asset.update(asset_id)
        return jsonify({
            'data': asset.__dict__,
            'message': f'{asset_class.object_name} updated successfully'
        }), 200
    except Exception as e:
        logger.error(f"Error occurred while updating asset: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while updating the asset.'}), 500


def delete_asset(asset_class, asset_id):
    try:
        asset = asset_class().get(asset_id)
        if asset:
            asset.delete()
            return jsonify({
                'data': asset.__dict__,
                'message': f'{asset_class.object_name} deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Asset not found'}), 404
    except Exception as e:
        logger.error(f"Error occurred while deleting asset: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while deleting the asset.'}), 500


def get_tree():
    try:
        assets = AssetTreeModel.get_tree()
        return jsonify({
            'data': assets,
            'message': 'All assets retrieved successfully'
        }), 200
    except Exception as e:
        logger.error(f"Failed to fetch all assets: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while fetching all assets.'}), 500

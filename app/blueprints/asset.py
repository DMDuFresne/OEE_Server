from flask import Blueprint, request
from app.services.asset import *
from app.limiter import limiter
from app.models.asset import EnterpriseModel, SiteModel, AreaModel, LineModel, CellModel


asset_blueprint = Blueprint('asset', __name__, url_prefix='/asset')


@asset_blueprint.route('/all', methods=['GET'])
def get_tree_route():
    return get_tree()


def create_asset_route(asset_class, create_func):
    @limiter.limit("60/minute")
    def route_create_asset():
        data = request.get_json()
        result = create_func(asset_class, data)
        return result

    endpoint_name = f'route_create_{asset_class.__name__.lower()}'
    route_path = f'/{asset_class.object_name.lower()}/create'
    asset_blueprint.add_url_rule(
        route_path,
        endpoint=endpoint_name,
        view_func=route_create_asset,
        methods=['POST']
    )
    # print(f"Created route: POST {route_path} => {endpoint_name}")


def get_all_assets_route(asset_class, get_all_func):
    @limiter.limit("60/minute")
    def route_get_all_assets():
        result = get_all_func(asset_class)
        return result

    endpoint_name = f'route_get_all_{asset_class.__name__.lower()}'
    route_path = f'/{asset_class.object_name.lower()}/all'
    asset_blueprint.add_url_rule(
        route_path,
        endpoint=endpoint_name,
        view_func=route_get_all_assets,
        methods=['GET']
    )
    # print(f"Created route: GET {route_path} => {endpoint_name}")


def get_asset_route(asset_class, get_func):
    @limiter.limit("60/minute")
    def route_get_asset(asset_id):
        result = get_func(asset_class, asset_id)
        return result

    endpoint_name = f'route_get_{asset_class.__name__.lower()}'
    route_path = f'/{asset_class.object_name.lower()}/<int:asset_id>'
    asset_blueprint.add_url_rule(
        route_path,
        endpoint=endpoint_name,
        view_func=route_get_asset,
        methods=['GET']
    )
    # print(f"Created route: GET {route_path} => {endpoint_name}")


def update_asset_route(asset_class, update_func):
    @limiter.limit("60/minute")
    def route_update_asset(asset_id):
        data = request.get_json()
        result = update_func(asset_class, data, asset_id)
        return result

    endpoint_name = f'route_update_{asset_class.__name__.lower()}'
    route_path = f'/{asset_class.object_name.lower()}/<int:asset_id>'
    asset_blueprint.add_url_rule(
        route_path,
        endpoint=endpoint_name,
        view_func=route_update_asset,
        methods=['PUT']
    )
    # print(f"Created route: PUT {route_path} => {endpoint_name}")


def delete_asset_route(asset_class, delete_func):
    @limiter.limit("60/minute")
    def route_delete_asset(asset_id):
        result = delete_func(asset_class, asset_id)
        return result

    endpoint_name = f'route_delete_{asset_class.__name__.lower()}'
    route_path = f'/{asset_class.object_name.lower()}/<int:asset_id>'
    asset_blueprint.add_url_rule(
        route_path,
        endpoint=endpoint_name,
        view_func=route_delete_asset,
        methods=['DELETE']
    )
    # print(f"Created route: DELETE {route_path} => {endpoint_name}")


# Create asset routes
create_asset_route(EnterpriseModel, create_asset)
create_asset_route(SiteModel, create_asset)
create_asset_route(AreaModel, create_asset)
create_asset_route(LineModel, create_asset)
create_asset_route(CellModel, create_asset)

# Get all asset routes
get_all_assets_route(EnterpriseModel, get_all_assets)
get_all_assets_route(SiteModel, get_all_assets)
get_all_assets_route(AreaModel, get_all_assets)
get_all_assets_route(LineModel, get_all_assets)
get_all_assets_route(CellModel, get_all_assets)

# Get asset routes
get_asset_route(EnterpriseModel, get_asset)
get_asset_route(SiteModel, get_asset)
get_asset_route(AreaModel, get_asset)
get_asset_route(LineModel, get_asset)
get_asset_route(CellModel, get_asset)

# Update asset routes
update_asset_route(EnterpriseModel, update_asset)
update_asset_route(SiteModel, update_asset)
update_asset_route(AreaModel, update_asset)
update_asset_route(LineModel, update_asset)
update_asset_route(CellModel, update_asset)

# Delete asset routes
delete_asset_route(EnterpriseModel, delete_asset)
delete_asset_route(SiteModel, delete_asset)
delete_asset_route(AreaModel, delete_asset)
delete_asset_route(LineModel, delete_asset)
delete_asset_route(CellModel, delete_asset)

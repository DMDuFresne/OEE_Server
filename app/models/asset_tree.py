from app.models.asset import *
from app.models.oee import OeeModel
from .asset_factory import asset_factory

load_dotenv()


class AssetTreeModel:
    @staticmethod
    def get_tree():

        try:

            query = "SELECT * FROM public.vw_obj_all"
            assets = AssetModel.fetch_all(query)

            hierarchy = {}

            for item in assets:
                enterprise = item['enterprise']
                site = item['site']
                area = item['area']
                line = item['line']
                cell = item['cell']

                asset_id = item['object_id']

                if enterprise not in hierarchy:

                    data = asset_factory.get_asset(4)().get(asset_id).to_dict()
                    oee = OeeModel.get_latest_oee(4, asset_id)

                    hierarchy[enterprise] = {}

                    if data:
                        hierarchy[enterprise]['data'] = data
                    if oee and data:
                        hierarchy[enterprise]['oee'] = oee

                if site is not None and site not in hierarchy[enterprise]:

                    data = asset_factory.get_asset(3)().get(asset_id).to_dict()
                    oee = OeeModel.get_latest_oee(3, asset_id)

                    hierarchy[enterprise][site] = {}

                    if data:
                        hierarchy[enterprise][site]['data'] = data
                    if oee and data:
                        hierarchy[enterprise][site]['oee'] = oee

                if area is not None and area not in hierarchy[enterprise][site]:

                    data = asset_factory.get_asset(2)().get(asset_id).to_dict()
                    oee = OeeModel.get_latest_oee(2, asset_id)

                    hierarchy[enterprise][site][area] = {}

                    if data:
                        hierarchy[enterprise][site][area]['data'] = data
                    if oee and data:
                        hierarchy[enterprise][site][area]['oee'] = oee

                if line is not None and line not in hierarchy[enterprise][site][area]:

                    data = asset_factory.get_asset(1)().get(asset_id).to_dict()
                    oee = OeeModel.get_latest_oee(1, asset_id)

                    hierarchy[enterprise][site][area][line] = {}

                    if data:
                        hierarchy[enterprise][site][area][line]['data'] = data
                    if oee and data:
                        hierarchy[enterprise][site][area][line]['oee'] = oee

                if cell is not None and line not in hierarchy[enterprise][site][area][line]:

                    data = asset_factory.get_asset(0)().get(asset_id).to_dict()
                    oee = OeeModel.get_latest_oee(0, asset_id)

                    hierarchy[enterprise][site][area][line][cell] = {}

                    if data:
                        hierarchy[enterprise][site][area][line][cell]['data'] = data
                    if oee and data:
                        hierarchy[enterprise][site][area][line][cell]['oee'] = oee

            return hierarchy

        except Exception as e:

            logger.error(f"Failed to fetch asset tree: {str(e)}", exc_info=True)
            raise Exception("An error occurred while fetching the asset tree.")

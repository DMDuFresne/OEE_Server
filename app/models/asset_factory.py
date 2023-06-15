import importlib


class AssetFactory:
    def __init__(self):
        self.asset_classes = {}

    def get_asset(self, object_type):
        if object_type not in self.asset_classes:
            if object_type == 0:
                module = importlib.import_module('app.models.asset')
                self.asset_classes[object_type] = module.CellModel
            elif object_type == 1:
                module = importlib.import_module('app.models.asset')
                self.asset_classes[object_type] = module.LineModel
            elif object_type == 2:
                module = importlib.import_module('app.models.asset')
                self.asset_classes[object_type] = module.AreaModel
            elif object_type == 3:
                module = importlib.import_module('app.models.asset')
                self.asset_classes[object_type] = module.SiteModel
            elif object_type == 4:
                module = importlib.import_module('app.models.asset')
                self.asset_classes[object_type] = module.EnterpriseModel
        return self.asset_classes[object_type]


asset_factory = AssetFactory()

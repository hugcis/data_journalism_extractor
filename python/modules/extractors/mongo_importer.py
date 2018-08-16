""" The Mongo loader operation module
"""
import os
from jinja2 import Environment
from modules.utils import format_types, quote
from modules.base_module import BaseModule


class MongoImporter(BaseModule):
    """ Main Mongo loader operation module class
    The Mongo loader allows to retreive an arbitrary number of fields
    from MongoDb Documents on convert the into a Flink DataSet.

    Args:
        module (dict): 
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.db_name = module.get('dbName')
        self.collection = module.get('collection')

        if self.db_name is None:
            raise ValueError(
                "No db name specified in module MongoImporter\
 {}".format(self.name))

        if not isinstance(module.get('requiredFields'), list):
            raise ValueError(
                "No required fields specified in module MongoImporter\
 {}".format(self.name))

        self.required_fields = [quote(i) for i in module.get('requiredFields')]

        self.data_type = ["String"]*len(module.get('requiredFields'))
        self.type = format_types(self.data_type)

        self.template_path = os.path.join('importers',
                                          'scala_mongo_loader.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            name=self.name,
            db_name=self.db_name,
            collection=self.collection,
            type=self.type,
            required_fields=self.required_fields
        ), ''

    def get_out_type(self):
        return self.data_type

    def check_integrity(self):
        pass

""" The JSON loader operation module
"""
import os
from typing import Tuple
from jinja2 import Environment
from modules.utils import format_types, quote
from .file_importer import FileImporter


class JsonImporter(FileImporter):
    """ Main JSON loader operation module class
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.main_field = module.get('mainField')
        if self.main_field is None:
            raise ValueError(
                "No main field specified in module JsonImporter\
 {}".format(self.name))

        if not isinstance(module.get('requiredFields'), list):
            raise ValueError(
                "No required fields specified in module JsonImporter\
 {}".format(self.name))

        self.required_fields = [quote(i) for i in module.get('requiredFields')]

        self.data_type = ["String"]*len(module.get('requiredFields'))

        self.template_path = os.path.join(self.template_path,
                                          'scala_json_loader.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> Tuple[str, str]:
        return self.template.render(
            file_path=self.file_path,
            name=self.name,
            main_field=self.main_field,
            type=format_types(self.data_type),
            required_fields=self.required_fields
        ), ''

    def get_out_type(self):
        return self.data_type

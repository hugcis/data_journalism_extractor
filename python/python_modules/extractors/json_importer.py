import os
from jinja2 import Environment
from .file_importer import FileImporter
from python_modules.utils import format_types, quote


class JsonImporter(FileImporter):
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
        self.type = format_types(self.data_type)

        self.template_path = os.path.join(self.template_path,
                                          'scala_json_loader.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            file_path=self.file_path,
            name=self.name,
            main_field=self.main_field,
            type=self.type,
            required_fields=self.required_fields
        ), ''

    def get_out_type(self):
        return self.data_type

import os
from jinja2 import Environment
from .file_importer import FileImporter
from python_modules.utils import format_types


class CsvImporter(FileImporter):
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.field_delimiter = module.get('fieldDelimiter')
        self.quote_character = module.get('quoteCharacter')

        if module.get('dataType') is None:
            raise ValueError(
                "No dataType provided for module {}".format(module))

        self.data_type = module.get('dataType')
        self.type = format_types(self.data_type)

        self.template_path = os.path.join(self.template_path,
                                          'scala_csv_loader.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            file_path=self.file_path,
            name=self.name,
            field_delimiter=self.field_delimiter,
            quote_character=self.quote_character,
            type=self.type
        ), ''

    def get_out_type(self):
        return self.data_type

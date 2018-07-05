import os
from jinja2 import Environment
from .file_output import FileOutput


class CsvOutput(FileOutput):
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.template_path = os.path.join(self.template_path,
                                          'scala_csv_output.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            file_path=self.file_path,
            name=self.name,
            source=self.source
        ), ''

    def get_out_type(self):
        return self.named_modules.get(self.source).get_out_type()

    def check_integrity(self):
        pass

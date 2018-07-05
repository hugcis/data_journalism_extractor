import os
from jinja2 import Environment
from .binary_operation import BinaryOperation
from python_modules.utils import format_types


class ExtractorLink(BinaryOperation):
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.left_fields = module.get('leftFields', 'all')
        self.right_fields = module.get('rightFields', 'all')

        template_path = os.path.join(self.template_path,
                                     'scala_extract.template')
        template_ext_path = os.path.join(self.template_path,
                                         'scala_extract_ext.template')

        self.template = self.env.get_template(template_path)
        self.template_ext = self.env.get_template(template_ext_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            name=self.name,
            source1=self.source1,
            source2=self.source2
        ), self.template_ext.render(
            name=self.name,
            typeLeft=format_types(
                self.named_modules.get(self.source1).get_out_type()),
            typeRight=format_types(
                self.named_modules.get(self.source2).get_out_type()),
            typeOut=format_types(self.get_out_type())
        )

    def get_out_type(self):
        type_left = self.get_type(self.source1, self.left_fields)
        type_right = self.get_type(self.source2, self.right_fields)

        return type_left + type_right

    def get_type(self, source, fields):
        source_type = self.named_modules.get(source).get_out_type()
        if fields == 'all':
            return source_type

        return [source_type[i-1] for i in fields]

    def check_integrity(self):
        pass

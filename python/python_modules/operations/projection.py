import os
from jinja2 import Environment
from .unary_operation import UnaryOperation
from python_modules.exceptions import IntegrityError


class Projection(UnaryOperation):
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.fields = module.get('fields')
        if self.fields is None:
            raise ValueError(
                "No fields provided in projection module {}".format(module))

        self.template_path = os.path.join(self.template_path,
                                          'scala_projection.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            name=self.name,
            source=self.source,
            projection_tuple=','.join(['set._{}'.format(i)
                                       for i in self.fields])
        ), ''

    def get_out_type(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        return [source_type[i-1] for i in self.fields]

    def check_integrity(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        if len(self.fields) >= len(source_type):
            raise IntegrityError(
                "Incorrect number of fields for module {}. {} were \
provided but the source has {}""".format(self.name,
                                         len(self.fields),
                                         len(source_type)))

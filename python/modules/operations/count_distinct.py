""" The distinct count operation module
"""
import os
from jinja2 import Environment
from .unary_operation import UnaryOperation


class CountDistinct(UnaryOperation):
    """ A module that count distinct elements of a dataflow
    and append it to the dataflow as a separate column.
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.fields = module.get('fields')
        if self.fields is None or len(self.fields) != 2:
            raise ValueError(
                "Wrong number of fields provided in projection module \
{}".format(module))

        self.template_path = os.path.join(self.template_path,
                                          'scala_count_distinct.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            name=self.name,
            source=self.source,
            field1=self.fields[0],
            field2=self.fields[1],
            in_fields=['t._{}'.format(i+1) for i in
                       range(len(self.named_modules.get(
                           self.source).get_out_type()))]
        ), ''

    def get_out_type(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        return source_type + ["Int"]

    def check_integrity(self):
        pass

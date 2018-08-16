""" The map operation module
"""
import os
from jinja2 import Environment
from modules.operations.unary_operation import UnaryOperation


class Map(UnaryOperation):
    """ A module that maps an arbitrary scala function to the
    incoming data flow.

    **Warning: Arbitrary scala code will only be checked at compilation
    and therefore could make the final program fail**
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.function = module.get('function')
        if self.function is None:
            raise ValueError(
                "No function provided in map module {}".format(self.name))

        self.out_type = module.get('outType')
        self.template_path = os.path.join(self.template_path,
                                          'scala_map.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            name=self.name,
            source=self.source,
            function=self.function
        ), ''

    def get_out_type(self):
        return self.out_type

    def check_integrity(self):
        pass

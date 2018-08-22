""" The map operation module
"""
import os
from typing import Tuple
from jinja2 import Environment
from modules.operations.unary_operation import UnaryOperation


class Map(UnaryOperation):
    """ A module that maps an arbitrary scala function to the
    incoming data flow.

    **Warning: Arbitrary scala code will only be checked at compilation
    and therefore could make the final program fail**

    Args:
        module (dict): The module dict must contain a ``function`` field
            that contains the desired scala function to be mapped to the data
            flow. (ex: ``"(tuple) => (tuple._1*2, tuple._2)"``).

            The ``outType`` field must also be provided to ensure
            compatibility with downstream modules.
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.function = module.get('function')
        if self.function is None:
            raise ValueError(
                "No function provided in map module {}".format(self.name))

        self.out_type = module.get('outType')
        if self.function is None:
            raise ValueError(
                "No outType provided in map module {}".format(self.name))

        self.template_path = os.path.join(self.template_path,
                                          'scala_map.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> Tuple[str, str]:
        return self.template.render(
            name=self.name,
            source=self.source,
            function=self.function
        ), ''

    def get_out_type(self):
        return self.out_type

    def check_integrity(self):
        pass

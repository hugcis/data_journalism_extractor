""" The simple NER operation module
"""
import os
from typing import Tuple
from jinja2 import Environment
from extractor_exceptions import IntegrityError
from modules.operations.unary_operation import UnaryOperation


class SimpleNER(UnaryOperation):
    """ A module that performs a simple NER extraction on a column
    of an incoming dataflow.

    Args:
        module (dict): The module dict must contain a ``field`` that
            specify the column index on which to perform the NER extraction
            (ex: ``0``)

    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.field = module.get('field')

        if self.field is None:
            raise ValueError(
                "No fields provided in simple ner module {}".format(module))

        self.template_path = os.path.join(self.template_path,
                                          'scala_simple_ner.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> Tuple[str, str]:
        below = ', '.join(['t_{}'.format(i + 1) for
                           i in range(self.field)])
        above = ', '.join(['t_{}'.format(i + 1) for
                           i in range(self.field, len(self.get_out_type()))])
        if above:
            above = ', ' + above
        if below:
            below = below + ', '

        return self.template.render(
            name=self.name,
            source=self.source,
            field=self.field,
            below=below,
            above=above
        ), ''

    def get_out_type(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        source_type[self.field] = "Array[String]"

        return source_type

    def check_integrity(self):
        source_type = self.named_modules.get(self.source).get_out_type()
        if source_type[self.field] != "String":
            raise IntegrityError(
                "Trying to do NER on incorrect type for module {}. {} not \
supported".format(self.name, source_type[self.field - 1]))

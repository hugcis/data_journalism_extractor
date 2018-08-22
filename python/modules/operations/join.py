""" The join operation module
"""
import os
from typing import Tuple
from jinja2 import Environment
from modules.operations.binary_operation import BinaryOperation


class Join(BinaryOperation):
    """ A module that joins two incoming dataflows on field1 == field2

    Args:
        module (dict): The module dict must contain the ``field1`` and
            ``field2`` fields that correspond to the desired index to
            make the join on.

            Other optional fields are:
                * ``leftFields`` and ``rightFields`` are lists of integers
                  specifying the indexes to keep in the join's output. Default
                  value is ``"all"``.
                  (ex: ``[0, 2]``)
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        self.field1 = module.get('field1')
        self.field2 = module.get('field2')

        self.left_fields = module.get('leftFields', 'all')
        self.right_fields = module.get('rightFields', 'all')

        self.template_path = os.path.join(self.template_path,
                                          'scala_join.template')

        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> Tuple[str, str]:
        return self.template.render(
            name=self.name,
            source1=self.source1,
            source2=self.source2,
            field1=self.field1,
            field2=self.field2,
            out_fields=', '.join(self._get_out_fields())
        ), ''

    def get_out_type(self):
        type_left = self.named_modules.get(self.source1).get_out_type()
        type_right = self.named_modules.get(self.source2).get_out_type()

        return (_compute_out_types(self.left_fields, type_left) +
                _compute_out_types(self.right_fields, type_right))

    def check_integrity(self):
        pass

    def _get_out_fields(self):
        return ([
            'l._{}'.format(i + 1) for i in
            self._field_numbers(self.left_fields, self.source1)
        ] + [
            'r._{}'.format(i + 1) for i in
            self._field_numbers(self.right_fields, self.source2)
        ])

    def _field_numbers(self, fields, source):
        in_type = self.named_modules.get(source).get_out_type()
        if fields == 'all':
            return list(range(len(in_type)))
        return fields


def _compute_out_types(fields, type_list):
    """ Utility function for returning the right
    field types from the `type_list`.

    `fields`is either a list of indexes or `"all"`.
    """
    if fields == 'all':
        return type_list
    return [type_list[i] for i in fields]

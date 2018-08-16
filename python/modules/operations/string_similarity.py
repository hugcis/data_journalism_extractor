""" The string similarity operation module
"""
import os
from jinja2 import Environment
from extractor_exceptions import IntegrityError
from .binary_operation import BinaryOperation


class StringSimilarity(BinaryOperation):
    """ A module that compute similarity scores between two string inputs
    with one of the available soft string matching algorithms.

    **Warning: Some algorithms compute a distance, some others a similarity
    score. Besides, some are normalized and some aren't. See the documentation
    for more details on each algorithm.**
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        # Fields to be compared
        self.left_field = module.get('leftField')
        self.right_field = module.get('rightField')

        # Selected fields for output
        self.left_out_fields = module.get('leftOutFields', 'all')
        self.right_out_fields = module.get('rightOutFields', 'all')

        self.algorithm = module.get('algorithm', 'Levenshtein')

        template_path = os.path.join(self.template_path,
                                     'scala_string_similarity.template')

        self.template = self.env.get_template(template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            name=self.name,
            source1=self.source1,
            source2=self.source2,
            left_field=self.left_field,
            right_field=self.right_field,
            left_out_fields=['l._{}'.format(i + 1) for i in
                             self._get_types(self.source1,
                                             self.left_out_fields)],
            right_out_fields=['r._{}'.format(i + 1) for i in
                              self._get_types(self.source2,
                                              self.right_out_fields)],
            algo_name=self.algorithm
        ), ''

    def get_out_type(self):
        type_left = self.named_modules.get(self.source1).get_out_type()
        type_right = self.named_modules.get(self.source2).get_out_type()

        out_left = [type_left[i] for i in
                    self._get_types(self.source1, self.left_out_fields)]
        out_right = [type_right[i] for i in
                     self._get_types(self.source2, self.right_out_fields)]

        return out_left + out_right + ['Double']

    def _get_types(self, source, out_fields):
        if out_fields == 'all':
            return list(range(len(
                self.named_modules.get(source).get_out_type())))
        return out_fields

    def check_integrity(self):
        type_left = self.named_modules.get(self.source1).get_out_type()
        type_right = self.named_modules.get(self.source2).get_out_type()

        if (not type_left[self.left_field] == 'String' or
                not type_right[self.right_field] == 'String'):
            raise IntegrityError(
                "This operation must have strings as inputs.\n Got {} and \
{}".format(type_left[self.left_field], type_right[self.right_field]))
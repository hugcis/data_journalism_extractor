""" The word similarity operation module
"""
import os
from jinja2 import Environment
from extractor_exceptions import IntegrityError
from .binary_operation import BinaryOperation


class ExtractorWordSimilarity(BinaryOperation):
    """ A module that extracts pairs of entities based on a similarity score
    of two sets of strings.
    The source extraction will always be the right flow and the target will be
    the left flow.
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        # Get selected fields that contain the array of word to
        # be compared
        self.left_field = module.get('leftField')
        self.right_field = module.get('rightField')

        # Source and target for extraction
        self.source_extract = module.get('sourceExtract')
        self.target_extract = module.get('targetExtract')

        template_path = os.path.join(self.template_path,
                                     'scala_extract_word_sim.template')

        self.template = self.env.get_template(template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            name=self.name,
            source1=self.source1,
            source2=self.source2,
            field1=self.left_field,
            field2=self.right_field
        ), ''

    def get_out_type(self):
        type_left = self.named_modules.get(self.source1).get_out_type()
        type_right = self.named_modules.get(self.source2).get_out_type()

        return [type_left, type_right, 'Double']

    def check_integrity(self):
        type_left = self.named_modules.get(self.source1).get_out_type()
        type_right = self.named_modules.get(self.source2).get_out_type()

        if (not type_left[self.left_field - 1] == 'Array[String]' or
                not type_right[self.right_field - 1] == 'Array[String]'):
            raise IntegrityError(
                "This operation must have arrays as inputs.\n Got {} and \
{}".format(type_left[self.left_field - 1], type_right[self.right_field - 1]))

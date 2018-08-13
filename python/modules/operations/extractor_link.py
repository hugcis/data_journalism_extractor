""" The mention link extractor operation module
"""
import os
from jinja2 import Environment
from modules.utils import format_types
from .binary_operation import BinaryOperation


class ExtractorLink(BinaryOperation):
    """ A module that extracts the occurrences of a given field of a data flow
    into a field of an other data flow.
    The source extraction will always be the right flow and the target will be
    the left flow.
    """
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        # Get selected fields for the left and right dataflows
        # (project while extracting)
        self.left_fields = module.get('leftFields', 'all')
        self.right_fields = module.get('rightFields', 'all')

        # Source and target for extraction
        self.source_extract = module.get('sourceExtract')
        self.target_extract = module.get('targetExtract')

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
            type_left=format_types(
                self.named_modules.get(self.source1).get_out_type()),
            type_right=format_types(
                self.named_modules.get(self.source2).get_out_type()),
            type_out=format_types(self.get_out_type()),
            source_extract=self.source_extract,
            target_extract=self.target_extract,
            collect_tuple=self._get_collection_tuple(),
            source1=self.source1,
            source2=self.source2
        )

    def get_out_type(self):
        type_left = self._get_type(self.source1, self.left_fields)
        type_right = self._get_type(self.source2, self.right_fields)

        return type_left + type_right

    def _get_type(self, source, fields):
        source_type = self.named_modules.get(source).get_out_type()
        if fields == 'all':
            return source_type

        return [source_type[i-1] for i in fields]

    def _indices(self, source, fields):
        if fields == 'all':
            source_type = self.named_modules.get(source).get_out_type()
            return range(1, len(source_type) + 1)
        return fields

    def _get_collection_tuple(self):
        return ','.join(
            [','.join(['value._1._{}'.format(i) for i in
                       self._indices(self.source1, self.left_fields)]),
             ','.join(['value._2._{}'.format(i) for i in
                       self._indices(self.source2, self.right_fields)])])

    def check_integrity(self):
        pass

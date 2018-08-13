""" The CSV loader operation module
"""
import os
from jinja2 import Environment
from modules.utils import format_types
from .file_importer import FileImporter


class CsvImporter(FileImporter):
    """ Main CSV loader operation module class.

    Args:
        module (dict): The module dict must have a ``dataType``
            field that contains the input types as a list of strings.

            Other optional fields are:
                * ``fieldDelimiter`` (csv delimiter if other than comma)
                * ``quoteCharacter`` (don't separate within quoted fields)
                * ``namedFields`` (for selecting only some of the columns
                  by their name)

    """
    # Reasonable amount of class attributes
    # pylint: disable=R0902
    def __init__(self, module, env: Environment, named_modules):
        super().__init__(module, env, named_modules)

        # delimiter and quote have default values if not in module
        self.field_delimiter = module.get('fieldDelimiter')
        self.quote_character = module.get('quoteCharacter')

        self.named_fields = module.get('namedFields')

        # By default, all columns and lines are imported
        self.column_list = None
        self.ignore_first_line = None

        # if fields are named in the modules, ignore first line and
        # compute the column numbers to be passed to the reader
        # (!! This implies opening the file first)
        # TODO: Implement for remote file
        if self.named_fields is not None:
            self.ignore_first_line = True
            self.column_list = self._get_column_list()

        self.data_type = module.get('dataType')
        if self.data_type is None:
            raise ValueError(
                "No dataType provided for module {}".format(module))
        self.formatted_type = format_types(self.data_type)

        self.template_path = os.path.join(self.template_path,
                                          'scala_csv_loader.template')
        self.template = self.env.get_template(self.template_path)

    def rendered_result(self) -> (str, str):
        return self.template.render(
            file_path=self.file_path,
            name=self.name,
            field_delimiter=self.field_delimiter,
            quote_character=self.quote_character,
            type=self.formatted_type,
            included_fields=self.column_list,
            ignore_first_line=self.ignore_first_line
        ), ''

    def get_out_type(self):
        return self.data_type

    def _get_column_list(self):
        """ Compute the column numbers corresponding to the named
        fields

        For a csv with column `a` and `b` and the required named
        field `b`, the column list is then `[1]`.
        """
        with open(self.file_path) as fle:
            fields = fle.readline().strip().split(self.field_delimiter)
        column_list = []
        for i, field in enumerate(fields):
            if field in self.named_fields:
                column_list.append(i)
        return tuple(column_list)   # Tuple for rendering (...) in a
        # template

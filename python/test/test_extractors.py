import unittest
import unittest.mock
from jinja2 import Environment
from python_modules.extractors import CsvImporter, JsonImporter
from python_modules.utils import format_types, quote


class TestCsvImporter(unittest.TestCase):
    """ Test suite for the CsvImporter
    """
    def setUp(self):
        self.env = Environment()
        self.module = {
            "name": "name",
            "path": "path/to/file.csv",
            "dataType": ["String"]
        }
        self.template_mock = unittest.mock.MagicMock()
        self.template_mock.render = unittest.mock.MagicMock(
            return_value="")

    @unittest.mock.patch.object(Environment, 'get_template')
    def test_init(self, mock_get_template: unittest.mock.patch):
        """ Should init correctly with minimal parameters
        """
        mock_get_template.return_value = self.template_mock
        csv_importer = CsvImporter(self.module, self.env, [])
        mock_get_template.assert_called()

        self.assertEqual(csv_importer.get_out_type(),
                         self.module.get("dataType"))

    @unittest.mock.patch.object(Environment, 'get_template')
    def test_render(self, mock_get_template: unittest.mock.patch):
        """ Should call render method with right parameters
        """
        mock_get_template.return_value = self.template_mock
        csv_importer = CsvImporter(self.module, self.env, [])
        result = csv_importer.rendered_result()

        self.assertEqual(result, ("", ""))
        self.template_mock.render.assert_called_once_with(
            file_path=self.module.get('path'),
            name=self.module.get('name'),
            field_delimiter=self.module.get('fieldDelimiter'),
            quote_character=self.module.get('quoteCharacter'),
            type=format_types(self.module.get('dataType'))
        )


class TestJsonImporter(unittest.TestCase):
    """ Test suite for the JsonImporter
    """
    def setUp(self):
        self.env = Environment()
        self.module = {
            "name": "name",
            "path": "path/to/file.json",
            "mainField": "main",
            "requiredFields": ["a", "b"]
        }
        self.template_mock = unittest.mock.MagicMock()
        self.template_mock.render = unittest.mock.MagicMock(
            return_value="")

    @unittest.mock.patch.object(Environment, 'get_template')
    def test_init(self, mock_get_template: unittest.mock.patch):
        """ Should init correctly with minimal parameters
        """
        mock_get_template.return_value = self.template_mock
        json_importer = JsonImporter(self.module, self.env, [])
        mock_get_template.assert_called()

        self.assertEqual(json_importer.get_out_type(),
                         len(self.module.get('requiredFields'))*["String"])

    @unittest.mock.patch.object(Environment, 'get_template')
    def test_render(self, mock_get_template: unittest.mock.patch):
        """ Should call render method with right parameters
        """
        mock_get_template.return_value = self.template_mock
        json_importer = JsonImporter(self.module, self.env, [])
        result = json_importer.rendered_result()

        self.assertEqual(result, ("", ""))
        self.template_mock.render.assert_called_once_with(
            file_path=self.module.get('path'),
            name=self.module.get('name'),
            main_field=self.module.get('mainField'),
            required_fields=[
                quote(i) for i in
                self.module.get('requiredFields')
            ],
            type=format_types(
                len(self.module.get('requiredFields'))*["String"])
        )

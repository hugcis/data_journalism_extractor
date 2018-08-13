import unittest
import json
import os
from renderer import Renderer
from extractor_exceptions import UnknownModuleError

TEMPLATE_DIR = 'templates'


class TestRenderer(unittest.TestCase):
    def test_init_empty(self):
        Renderer([], TEMPLATE_DIR)

    def test_init_wrong_modules(self):
        with self.assertRaises(UnknownModuleError):
            Renderer([{}], TEMPLATE_DIR)

        with self.assertRaises(UnknownModuleError):
            Renderer([{"type": "foo"}], TEMPLATE_DIR)

    def test_init(self):
        f_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'fixtures/test_spec.json'
        )
        with open(f_name) as json_file:
            test_spec = json.load(json_file).get('modules')

        render = Renderer(test_spec, TEMPLATE_DIR)

        self.assertCountEqual(render.name_list,
                              render.named_modules.keys())

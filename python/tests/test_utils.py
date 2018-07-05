import unittest
from python_modules.utils import format_types, quote


class TestFormatTypes(unittest.TestCase):
    def test_one_type(self):
        self.assertEqual("Tuple1[String]", format_types(["String"]))

    def test_multiple_types(self):
        for i in range(2, 5):
            self.assertEqual(
                "({})".format(','.join(i*["TEST"])),
                format_types(i*["TEST"]))


class TestQuote(unittest.TestCase):
    def test_quote(self):
        self.assertEqual("\"TEST\"", quote("TEST"))

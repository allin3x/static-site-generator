import unittest
from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_markdown(self):
        markdown = """ # Hello World\n ## Jello\n"""

        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")

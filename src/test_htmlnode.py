# unittests, run from test.sh in root folder
import unittest

from htmlnode import HTMLNode


# split tests in multiple cases to always see all tests/know which one is wrong
class TestHTMLNode(unittest.TestCase):
    # single dictionary (1 key/value pair)
    def test_props_single(self):
        props_1_pair = {"href": "www.testing.com"}
        self.assertEqual(
            HTMLNode(props=props_1_pair).props_to_html(), ' href="www.testing.com"'
        )

    # multiple dictionary (3 key/value pair)
    def test_props_multiple(self):
        props_3_pair = {
            "href": "www.testing.com",
            "target": "_blank",
            "whatup": "testing",
        }
        self.assertEqual(
            HTMLNode(props=props_3_pair).props_to_html(),
            ' href="www.testing.com" target="_blank" whatup="testing"',
        )

    # empty dictionary (no key/value pair)
    def test_props_empty(self):
        props_empty = {}
        self.assertEqual(HTMLNode(props=props_empty).props_to_html(), "")


if __name__ == "__main__":
    unittest.main()

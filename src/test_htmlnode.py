# unittests, run from test.sh in root folder
import unittest

from htmlnode import HTMLNode, LeafNode


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

    # --------------------- Test LeafNode ------------------#
    # example test
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "What up!")
        self.assertEqual(node.to_html(), "<p>What up!</p>")

    # empty value test (raise valueerror)
    def test_leaf_empty_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    # empty tag test (return value as string)
    def test_leaf_empty_tag(self):
        node = LeafNode(None, "hello")
        self.assertEqual(node.to_html(), "hello")

    # tag with props
    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.kagi.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.kagi.com">Click me!</a>')

    # multiple props
    def test_leaf_multiple_props(self):
        node = LeafNode("img", "", {"src": "image.png", "alt": "a photo"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="a photo"></img>')


if __name__ == "__main__":
    unittest.main()

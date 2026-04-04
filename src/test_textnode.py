# unittests, run from test.sh in root folder

import unittest

from textnode import TextNode, TextType


# test TextNode class
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    # check if nodes are not equal
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    # check if passed url is none
    def test_is_none(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()

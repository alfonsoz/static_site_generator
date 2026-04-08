import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestConversions(unittest.TestCase):
    # TextNode(s) to HTMLNode
    def test_text(self):
        node = TextNode("this is a textnode", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "this is a textnode")

    def test_bold(self):
        node = TextNode("this is a textnode in bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is a textnode in bold")
        self.assertEqual(html_node.to_html(), "<b>this is a textnode in bold</b>")

    def test_italic(self):
        node = TextNode("this is a textnode in italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        # print(f"{html_node.value}")
        # print(f"{html_node.tag}")
        # print(f"{html_node.to_html()}")
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is a textnode in italic")
        self.assertEqual(html_node.to_html(), "<i>this is a textnode in italic</i>")

    def test_code(self):
        node = TextNode("this is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "this is code text")
        self.assertEqual(html_node.to_html(), "<code>this is code text</code>")

    def test_link(self):
        node = TextNode("this is a link", TextType.LINK, "www.kagi.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this is a link")
        self.assertEqual(html_node.props, {"href": node.url})
        self.assertEqual(
            html_node.to_html(), '<a href="www.kagi.com">this is a link</a>'
        )

    def test_img(self):
        node = TextNode("this is an image", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "image.png", "alt": "this is an image"}
        )
        self.assertEqual(
            html_node.to_html(), '<img src="image.png" alt="this is an image"></img>'
        )
        # print(f"{html_node.to_html()}")

    def test_wrong_input(self):
        node = TextNode("this should be a wrong type", "WRONG")
        with self.assertRaises(Exception) as e:
            html_node = text_node_to_html_node(node)
        # print(e.exception)

import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown_parser import split_nodes_delimiter


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

    # ============= Split_nodes_delimiter tests ================
    # ============= markdown_parser.py          ================
    def test_text_without_delimiter(self):
        node = [TextNode("this is some text", TextType.TEXT)]
        new_node = split_nodes_delimiter(node, "'", TextType.TEXT)
        # print(f"{new_node}")
        self.assertEqual(new_node[0].text, "this is some text")

    def test_text_with_code_delimiter(self):
        node = [TextNode("this is some text with a 'code' block", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(node, "'", TextType.CODE)
        # print(f"{new_nodes}")
        result1 = TextNode("this is some text with a ", TextType.TEXT)
        result2 = TextNode("code", TextType.CODE)
        result3 = TextNode(" block", TextType.TEXT)
        self.assertEqual(new_nodes, [result1, result2, result3])

    def test_text_with_bold_delimiter(self):
        node = [
            TextNode(
                "this is some text with a **bolded phrase** and nothing else",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        # print(f"{new_nodes}")
        result1 = TextNode("this is some text with a ", TextType.TEXT)
        result2 = TextNode("bolded phrase", TextType.BOLD)
        result3 = TextNode(" and nothing else", TextType.TEXT)
        self.assertEqual(new_nodes, [result1, result2, result3])

    def test_text_with_italic_delimiter(self):
        node = [
            TextNode(
                "this is some text with an _italic phrase_ and nothing else",
                TextType.TEXT,
            )
        ]
        new_nodes = split_nodes_delimiter(node, "_", TextType.ITALIC)
        # print(f"{new_nodes}")
        result1 = TextNode("this is some text with an ", TextType.TEXT)
        result2 = TextNode("italic phrase", TextType.ITALIC)
        result3 = TextNode(" and nothing else", TextType.TEXT)
        self.assertEqual(new_nodes, [result1, result2, result3])

    def test_text_with_different_delimiters(self):
        node = [
            TextNode(
                "this is some text with a **bolded phrase** an _italic phrase_ and a 'code block'.",
                TextType.TEXT,
            )
        ]
        # chain them together
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "'", TextType.CODE)
        # print(f"{new_nodes}")
        result1 = TextNode("this is some text with a ", TextType.TEXT)
        result2 = TextNode("bolded phrase", TextType.BOLD)
        result3 = TextNode(" an ", TextType.TEXT)
        result4 = TextNode("italic phrase", TextType.ITALIC)
        result5 = TextNode(" and a ", TextType.TEXT)
        result6 = TextNode("code block", TextType.CODE)
        result7 = TextNode(".", TextType.TEXT)
        self.assertEqual(
            new_nodes, [result1, result2, result3, result4, result5, result6, result7]
        )

    def test_text_mixed_nodes(self):
        node = TextNode("this has a **bold** phrase inside", TextType.BOLD)
        node2 = TextNode("this has a 'code block' in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        result1 = TextNode("this has a **bold** phrase inside", TextType.BOLD)
        result2 = TextNode("this has a 'code block' in it", TextType.TEXT)
        self.assertEqual(new_nodes, [result1, result2])

    def test_text_mixed_nodes_2(self):
        node = TextNode("this has a **bold** __phrase_ 'inside", TextType.BOLD)
        node2 = TextNode("this ** has a 'code block' in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "'", TextType.CODE)
        result1 = TextNode("this has a **bold** __phrase_ 'inside", TextType.BOLD)
        result2 = TextNode("this ** has a ", TextType.TEXT)
        result3 = TextNode("code block", TextType.CODE)
        result4 = TextNode(" in it", TextType.TEXT)
        self.assertEqual(new_nodes, [result1, result2, result3, result4])

    def test_text_no_closing_delimiter(self):
        node = [
            TextNode(
                "this is some text with a 'code block that has no end delimiter",
                TextType.TEXT,
            )
        ]
        with self.assertRaises(Exception) as e:
            new_nodes = split_nodes_delimiter(node, "'", TextType.CODE)
        # print(e.exception)

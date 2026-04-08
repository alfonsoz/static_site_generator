# unittests, run from test.sh in root folder
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    # --------------------- Test ParentNode ------------------#
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        # print(f"{parent_node.to_html()}")
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_more_grandchildren(self):
        grandgrandchild_node = LeafNode("a", "smallest")
        grandchild_node = ParentNode("b", [grandgrandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        # print(f"{parent_node.to_html()}")
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><a>smallest</a></b></span></div>",
        )

    # multiple children at the same level
    def test_to_html_multiple_children(self):
        leaf1 = LeafNode("a", "smallest")
        leaf2 = LeafNode("span", "hello")
        leaf3 = LeafNode("div", "test")
        parent_node = ParentNode("etc", [leaf1, leaf2, leaf3])
        # print(f"{parent_node.to_html()}")
        self.assertEqual(
            parent_node.to_html(),
            "<etc><a>smallest</a><span>hello</span><div>test</div></etc>",
        )

    # mixed children, parentnode whose children include both parent and childnode objects at the same level
    def test_to_html_mixed_children(self):
        child_leaf_node = LeafNode("a", "smallest")
        mixed_node = ParentNode("span", [LeafNode(None, "plain"), child_leaf_node])
        parent_node = ParentNode("div", [mixed_node])
        # print(f"{parent_node.to_html()}")
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>plain<a>smallest</a></span></div>",
        )

    # Leafnode with Nonetag as child
    def test_to_html_leaf_none_child(self):
        child_node = LeafNode(None, "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div>child</div>")

    def test_parent_no_tag(self):
        childnode = LeafNode("b", "hello")
        parentnode = ParentNode(None, [childnode])
        with self.assertRaises(ValueError) as e:
            parentnode.to_html()
        # print(e.exception)

    def test_parent_no_child(self):
        parentnode = ParentNode("a", None)
        with self.assertRaises(ValueError) as e:
            parentnode.to_html()
        # print(e.exception)


if __name__ == "__main__":
    unittest.main()

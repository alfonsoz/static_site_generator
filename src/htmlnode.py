# HTML node class, all data members are optional and None as default
# HTMLNode represents a node in an HTML tree, including its tag, content,
# child nodes, and optional attributes that can be rendered as HTML.
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise (NotImplementedError)

    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self) -> str:
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"


# the LeafNode is a type of HTMLNode that represents a single HTML tag with no children.
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value. Leaf node has no value.")
        if self.tag is None:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props})"


# ParentNode, any node that is not a 'leaf' node (or has children) is a parentnode
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag. ParentNode has no tag")
        if self.children is None:
            raise ValueError(f"Invalid HTML: no children. ParentNode has no children")

        # string representing the html tag
        result_string = ""
        for child in self.children:
            result_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{result_string}</{self.tag}>"

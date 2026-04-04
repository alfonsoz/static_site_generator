import htmlnode
import textnode


def main():
    test_node = textnode.TextNode(
        "This is some anchor text", textnode.TextType.LINK, "https://www.boot.dev"
    )

    test_props = {
        "href": "https://www.kagi.com",
        "target": "_blank",
    }
    test_htmlnode = htmlnode.HTMLNode("hello", "42", test_node, test_props)

    print(test_node)
    print(test_htmlnode)


# if main, only run when it is executed directly, not when it is imported somehow
if __name__ == "__main__":
    main()

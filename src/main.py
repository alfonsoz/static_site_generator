import textnode


def main():
    test_node = textnode.TextNode(
        "This is some anchor text", textnode.TextType.LINK, "https://www.boot.dev"
    )
    print(test_node)


# if main, only run when it is executed directly, not when it is imported somehow
if __name__ == "__main__":
    main()

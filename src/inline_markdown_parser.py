from textnode import TextNode, TextType
import re


# raw markdown to TextNodes
# take a list of nodes, find one specific delimiter, return new list with the splits applied.
# example calls:
# - nodes = split_nodes_delimiter([node], "`", TextType.CODE)
# - nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    # loop through nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            # split on the delimiter
            sections = node.text.split(delimiter)
            # even length = invalid, raise exception (a delimiter was not closed)
            # the split should otherwise end up in an odd number
            if len(sections) % 2 == 0:
                raise Exception("invalid markdown syntax, no closing delimiter found")
            # odd length = valid
            else:
                for i in range(len(sections)):
                    # skip empty string
                    if sections[i] == "":
                        continue
                    # even = TextType.TEXT
                    if i % 2 == 0:
                        new_node = TextNode(sections[i], TextType.TEXT)
                    # odd = delimited type (passed by the function)
                    else:
                        new_node = TextNode(sections[i], text_type)
                    result.append(new_node)
    return result


# takes raw markdown text to extract images
# returns list of tuples
def extract_markdown_images(text):
    # \!\[[^\[\]]*\] = every character between square brackets ![]
    # \([^\(\)]*\) = every character between () and has no () inside
    # r"" pythonic for treat the string as a raw string, no escape sequence or backslash needed
    return re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# takes raw markdown text and extracts links
# return list of tuples with anchor text and url's
def extract_markdown_links(text):
    # (?<!!) = negative look behind, so there can be no ! before. (as that is an image)
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            resulting_text = node.text.split(delimiter)

            if len(resulting_text) % 2 == 0:
                raise Exception("The provided delimiter is unbalanced or incomplete in the text: " + node.text)

            temp_nodes = []

            for i, text in enumerate(resulting_text):
                if i % 2 == 0:
                    temp_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    temp_nodes.append(TextNode(text, text_type))
            new_nodes.extend(temp_nodes)

        elif node.text_type is not TextType.TEXT:
            new_nodes.append(node)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        temp_nodes = []

        if re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):

            resulting_text = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)

            for i, part in enumerate(resulting_text):
                if i % 3 == 0:
                    if part.strip():
                        temp_nodes.append(TextNode(part, TextType.TEXT))
                elif i % 3 == 1:
                    alt_text = part
                elif i % 3 == 2:
                    temp_nodes.append(TextNode(alt_text, TextType.IMAGE, part))

        else:
            temp_nodes.append(node)

        new_nodes.extend(temp_nodes)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        temp_nodes = []

        if re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text):

            resulting_text = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)

            for i, part in enumerate(resulting_text):
                if i % 3 == 0:
                    if part.strip():
                        temp_nodes.append(TextNode(part, TextType.TEXT))
                elif i % 3 == 1:
                    alt_text = part
                elif i % 3 == 2:
                    temp_nodes.append(TextNode(alt_text, TextType.LINK, part))

        else:
            temp_nodes.append(node)

        new_nodes.extend(temp_nodes)

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

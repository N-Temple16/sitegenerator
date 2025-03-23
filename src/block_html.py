from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from blocks import markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from blocktype import BlockType, block_to_block_type

def process_block(block, block_type):
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return create_unordered_list_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return create_ordered_list_node(block)
    elif block_type == BlockType.CODE:
        return create_code_node(block)
    elif block_type == BlockType.HEADING:
        return create_heading_node(block)
    else:
        return create_paragraph_node(block)

def create_quote_node(block):
    lines = block.split('\n')
    text = '\n'.join([line[1:].strip() if line.startswith('>') else line for line in lines])
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def create_unordered_list_node(block):
    items = []
    lines = block.split("\n")

    for line in lines:
        if line.strip() and line.strip().startswith("- "):
            item_text = line.strip()[2:]
            item_children = text_to_children(item_text)
            item_node = ParentNode("li", item_children)
            items.append(item_node)
    return ParentNode("ul", items)

def create_ordered_list_node(block):
    items = []
    lines = block.split("\n")

    for line in lines:
        if line.strip() and line.strip()[0].isdigit() and ". " in line.strip():
            pos = line.find(". ") + 2
            item_text = line[pos:]
            item_children = text_to_children(item_text)
            item_node = ParentNode("li", item_children)
            items.append(item_node)
    return ParentNode("ol", items)

def create_code_node(block):
    lines = block.split("\n")
    code_content = "\n".join(lines[1:-1]) + "\n"

    text_node = TextNode(code_content, TextType.CODE)
    code_node = text_node_to_html_node(text_node)

    return ParentNode("pre", [code_node])

def create_heading_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    text = block[level+1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def create_paragraph_node(block):
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes

def markdown_to_html_node(markdown):
    split_markdown = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [], None)

    for block in split_markdown:
        block_type = block_to_block_type(block)
        html_node = process_block(block, block_type)
        parent_node.children.append(html_node)

    return parent_node

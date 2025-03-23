from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from block_html import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as from_file:
        from_contents = from_file.read()

    with open(template_path, 'r') as template_file:
        template_contents = template_file.read()

    convert_markdown = markdown_to_html_node(from_contents)
    content = convert_markdown.to_html()

    title = extract_title(from_contents)

    final_html = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", content)

    import os
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            header = line.lstrip("#").strip()
            return header
    raise Exception("There should be a header provided")

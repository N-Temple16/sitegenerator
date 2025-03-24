from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from block_html import markdown_to_html_node
import os
import shutil
import pathlib

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as from_file:
        from_contents = from_file.read()

    with open(template_path, 'r') as template_file:
        template_contents = template_file.read()

    convert_markdown = markdown_to_html_node(from_contents)
    content = convert_markdown.to_html()

    title = extract_title(from_contents)

    final_html = template_contents \
        .replace("{{ Title }}", title) \
        .replace("{{ Content }}", content) \
        .replace('href="/', f'href="{basepath}/') \
        .replace('src="/', f'src="{basepath}/')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        destination_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path):
            if pathlib.Path(source_path).suffix == ".md":
                destination_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
                generate_page(source_path, template_path, destination_path, basepath)
        else:
            os.makedirs(destination_path, exist_ok=True)
            generate_pages_recursive(source_path, template_path, destination_path, basepath)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            header = line.lstrip("#").strip()
            return header
    raise Exception("There should be a header provided")

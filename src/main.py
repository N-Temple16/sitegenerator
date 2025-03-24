from textnode import TextNode, TextType
from markdown_parser import generate_page, extract_title, generate_pages_recursive
import os
import shutil

def copy_to_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.mkdir(destination)
    print(f"Created directory: {destination}")

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
            print(f"Copied file: {source_path} to {destination_path}")
        else:
            copy_to_directory(source_path, destination_path)

def main():
    # Call your copy function with the appropriate paths
    copy_to_directory("static", "public")

    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()

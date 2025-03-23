import re

def extract_markdown_images(text):
    img_matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return img_matches

def extract_markdown_links(text):
    link_matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_matches

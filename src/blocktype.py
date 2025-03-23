from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith('#'):
        first_chars = block.split(' ', 1)[0]
        if all(char == '#' for char in first_chars) and 1 <= len(first_chars) <= 6:
            if len(block) > len(first_chars) and block[len(first_chars)] == ' ':
                return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith('>') for line in block.split('\n')):
        return BlockType.QUOTE
    elif all(line.startswith('- ') for line in block.split('\n')):
        return BlockType.UNORDERED_LIST
    elif block:
        lines = block.split("\n")
        is_ordered_list = True
        for i, line in enumerate(lines):
            expected_prefix = f"{i+1}. "
            if not line.startswith(expected_prefix):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

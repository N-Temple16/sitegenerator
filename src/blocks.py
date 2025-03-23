def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    result = []
    for block in blocks:
        cleaned_block = block.strip()
        if cleaned_block:
            lines = cleaned_block.split("\n")
            normalized_lines = [lines[0]] + [line.strip() for line in lines[1:]]
            cleaned_block = "\n".join(normalized_lines)
            result.append(cleaned_block)

    return result

import unittest
from blocktype import BlockType, block_to_block_type
from block_html import markdown_to_html_node

class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading 1"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("### Heading 3"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("###### Heading 6"),
            BlockType.HEADING
        )
        # Test invalid headings
        self.assertNotEqual(
            block_to_block_type("#No space after hash"),
            BlockType.HEADING
        )
        self.assertNotEqual(
            block_to_block_type("####### Too many hashes"),
            BlockType.HEADING
        )

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```\ncode block\n```"),
            BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("```code block```"),
            BlockType.CODE
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type(">This is a quote"),
            BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type(">This is a quote\n>This is another line"),
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- Item 1"),
            BlockType.UNORDERED_LIST
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- Item 1"),
            BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item 2\n- Item 3"),
            BlockType.UNORDERED_LIST
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. Item 1"),
            BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"),
            BlockType.ORDERED_LIST
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()

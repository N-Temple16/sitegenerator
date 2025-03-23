import unittest

from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from regex_links import extract_markdown_images, extract_markdown_links
from blocks import markdown_to_blocks

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = TextNode("This is a node", TextType.CODE)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node3, node4)

    def test_not_eq2(self):
        node5 = TextNode("This is a text node", TextType.TEXT)
        node6 = TextNode("This is not a text node", TextType.TEXT)
        self.assertNotEqual(node5, node6)

    def test_basic_delimiter_success(self):
        node = TextNode("This **is** bold", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" bold", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_italic_delimiter_success(self):
        node = TextNode("This _is_ italic", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.ITALIC),
            TextNode(" italic", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_no_delimiters(self):
        node = TextNode("This is just text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [TextNode("This is just text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_unbalanced_delimiter_raises_exception(self):
        node = TextNode("This **is bold", TextType.TEXT)

        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is even more text as well as an ![image](https://i.imgur.com/pYtHoN.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/pYtHoN.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_images(
            "This is text with a link ![to osrs](https://oldschool.runescape.com/)"
        )
        self.assertListEqual([("to osrs", "https://oldschool.runescape.com/")], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_images(
            "This is more text as well as a link ![to youtube](https://www.youtube.com/)"
        )
        self.assertListEqual([("to youtube", "https://www.youtube.com/")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images2(self):
        node = TextNode(
            "This is a line of text with an ![image](https://i.imgur.com/tEsTiMg.png) with a second ![second image](https://i.imgur.com/iMgTeSt.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a line of text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/tEsTiMg.png"),
                TextNode(" with a second ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/iMgTeSt.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images3(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/12345.png) and that's it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/12345.png"),
                TextNode(" and that's it", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Even more text with a link [to new rs](https://www.runescape.com/l=2/community) with this one too [to youtube](https://www.youtube.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Even more text with a link ", TextType.TEXT),
                TextNode("to new rs", TextType.LINK, "https://www.runescape.com/l=2/community"),
                TextNode(" with this one too ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/"
                ),
            ],
            new_nodes,
        )

    def test_split_links2(self):
        node = TextNode(
            "This is text with a link [to google](https://www.google.com/) and another [to osrs](https://oldschool.runescape.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to google", TextType.LINK, "https://www.google.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "to osrs", TextType.LINK, "https://oldschool.runescape.com/"
                ),
            ],
            new_nodes,
        )

    def test_split_links3(self):
        node = TextNode(
            "I am going to listen to music [on soundcloud](https://soundcloud.com/discover) kinda cool",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("I am going to listen to music ", TextType.TEXT),
                TextNode("on soundcloud", TextType.LINK, "https://soundcloud.com/discover"),
                TextNode(" kinda cool", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode(
            "This is text with no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode(
            "This is text with no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_textnodes(self):
        text = "Hello my `name` is _Nigel_ nice to meet **you** here is a cool _link_ I found [link](https://boot.dev) and a **rad** image ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
	    new_nodes,
            [
                TextNode("Hello my ", TextType.TEXT),
                TextNode("name", TextType.CODE),
		TextNode(" is ", TextType.TEXT),
                TextNode("Nigel", TextType.ITALIC),
                TextNode(" nice to meet ", TextType.TEXT),
                TextNode("you", TextType.BOLD),
                TextNode(" here is a cool ", TextType.TEXT),
		TextNode("link", TextType.ITALIC),
		TextNode(" I found ", TextType.TEXT),
		TextNode("link", TextType.LINK, "https://boot.dev"),
		TextNode(" and a ", TextType.TEXT),
		TextNode("rad", TextType.BOLD),
		TextNode(" image ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ]
        )

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here

    Hello I am another paragraph

    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here",
				"Hello I am another paragraph",
				"This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks3(self):
        md = """
    This is **bolded** paragraph
    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\n- This is a list\n- with items",
            ],
        )



if __name__ == "__main__":
    unittest.main()

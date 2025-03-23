import unittest
from markdown_parser import extract_title

class TestBlockToBlockType(unittest.TestCase):

    def test_heading1(self):
        markdown = "This is not a title\n# Hello I am a Title\nThis is nto a title either"

        title = extract_title(markdown)
        self.assertEqual(title, "Hello I am a Title")

    def test_heading2(self):
        markdown = "# A title"
        title = extract_title(markdown)
        self.assertEqual(title, "A title")

    def test_heading3(self):
        markdown = "There is no title here"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()

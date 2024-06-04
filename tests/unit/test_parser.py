import unittest
from unittest import mock
from markdown2confluence.parser import MarkdownParser


class TestMarkdownParser(unittest.TestCase):

    def setUp(self):
        self.parser = MarkdownParser()

    @mock.patch('markdown2confluence.parser.MarkdownParser._read_file_content')
    @mock.patch('os.walk')
    def test_parse_directory_invalid_path(
            self, mock_walk, mock_read_content):
        mock_read_content.side_effect = lambda file_path: \
            "Content of " + file_path
        mock_walk.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_directory('non_existing_directory')

    @mock.patch('markdown2confluence.parser.MarkdownParser._read_file_content')
    @mock.patch('os.walk')
    def test_parse_directory_empty(
            self, mock_walk, mock_read_content):
        mock_read_content.side_effect = lambda file_path: \
            "Content of " + file_path
        mock_walk.return_value = iter([])
        tree = self.parser.parse_directory('/emptydir')
        self.assertEqual(tree.root.name, 'root')
        self.assertEqual(tree.root.children, {})

    @mock.patch('markdown2confluence.parser.MarkdownParser._read_file_content')
    @mock.patch('os.walk')
    def test_parse_directory_with_non_markdown_files(
            self, mock_walk, mock_read_content):
        mock_read_content.side_effect = lambda file_path: \
            "Content of " + file_path
        mock_walk.return_value = iter(
            [('/dir_with_non_md_files', [], ['test.txt'])])
        tree = self.parser.parse_directory('/dir_with_non_md_files')
        self.assertEqual(tree.root.children, {})

    @mock.patch('markdown2confluence.parser.MarkdownParser._read_file_content')
    @mock.patch('os.walk')
    def test_parse_directory_with_nested_structure(
            self, mock_walk, mock_read_content):
        mock_read_content.side_effect = lambda file_path: \
            "Content of " + file_path
        mock_walk.return_value = iter([
            ('/nesteddir', ['nested'], []),
            ('/nesteddir/nested', [], ['test.md'])
        ])
        tree = self.parser.parse_directory('/nesteddir')
        self.assertIn('nested', tree.root.children)
        self.assertIn('test.md', tree.root.children['nested'].children)

    @mock.patch('markdown2confluence.parser.MarkdownParser._read_file_content')
    @mock.patch('os.walk')
    def test_parse_directory_with_multiple_markdown_files(
            self, mock_walk, mock_read_content):
        mock_read_content.side_effect = lambda file_path: \
            "Content of " + file_path
        mock_walk.return_value = iter([
            ('/dir_with_multiple_md', [], ['test1.md', 'test2.md'])
        ])
        tree = self.parser.parse_directory('/dir_with_multiple_md')
        self.assertIn('test1.md', tree.root.children)
        self.assertIn('test2.md', tree.root.children)
        self.assertEqual(
            tree.root.children['test1.md'].content,
            "Content of /dir_with_multiple_md/test1.md")
        self.assertEqual(
            tree.root.children['test2.md'].content,
            "Content of /dir_with_multiple_md/test2.md")

    def test_get_media_references_no_media(self):
        markdown = """
        # Title
        This is a test markdown without any media links.
        """
        result = self.parser._get_media_references(markdown)
        self.assertEqual(result, [])

    def test_get_media_references_with_local_media(self):
        markdown = """
        # Title
        ![Alt text](image1.png)
        Some text.
        ![Alt text](folder/image2.jpg)
        """
        result = self.parser._get_media_references(markdown)
        expected = ['image1.png', 'folder/image2.jpg']
        self.assertEqual(result, expected)

    def test_get_media_references_with_mixed_links(self):
        markdown = """
        # Title
        ![Alt text](image1.png)
        Some text.
        ![Alt text](http://example.com/image2.jpg)
        """
        result = self.parser._get_media_references(markdown)
        expected = ['image1.png']
        self.assertEqual(result, expected)

    def test_get_media_references_with_relative_links(self):
        markdown = """
        # Title
        ![Alt text](./relative/image1.png)
        Some text.
        ![Alt text](../parent/image2.jpg)
        """
        result = self.parser._get_media_references(markdown)
        expected = ['./relative/image1.png', '../parent/image2.jpg']
        self.assertEqual(result, expected)

    def test_get_media_references_nested_links(self):
        markdown = """
        # Title
        ![Alt text](folder/subfolder/image1.png)
        Some text.
        ![Alt text](folder/subfolder/deep/image2.jpg)
        """
        result = self.parser._get_media_references(markdown)
        expected = ['folder/subfolder/image1.png',
                    'folder/subfolder/deep/image2.jpg']
        self.assertEqual(result, expected)

    def test_get_media_references_with_empty_url(self):
        markdown = """
        # Title
        ![Alt text]()
        Some text.
        ![Alt text](folder/image2.jpg)
        """
        result = self.parser._get_media_references(markdown)
        expected = ['folder/image2.jpg']
        self.assertEqual(result, expected)

    def test_get_media_references_with_broken_markdown(self):
        markdown = """
        # Title
        ![Alt text](image1.png
        Some text.
        ![Alt text](folder/image2.jpg)
        """
        result = self.parser._get_media_references(markdown)
        expected = ['folder/image2.jpg']
        self.assertEqual(result, expected)

    def test_get_media_references_with_html_image_tag(self):
        markdown = """
        # Title
        <img src="image1.png" alt="Alt text">
        Some text.
        ![Alt text](folder/image2.jpg)
        """
        result = self.parser._get_media_references(markdown)
        expected = ['folder/image2.jpg']
        self.assertEqual(result, expected)

    def test_get_media_references_with_special_chars(self):
        markdown = """
        # Title
        ![Alt text](image_1.png)
        Some text.
        ![Alt text](folder/image-2.jpg)
        ![Alt text](folder/image.3.gif)
        ![Alt text](folder/image@4.bmp)
        ![Alt text](folder/image#5.jpeg)
        ![Alt text](folder/image$6.png)
        ![Alt text](folder/image&7.jpg)
        ![Alt text](folder/image(8).gif)
        ![Alt text](folder/image)9.bmp)
        ![Alt text](folder/image+10.jpeg)
        ![Alt text](folder/image,11.png)
        ![Alt text](folder/image;12.jpg)
        ![Alt text](folder/image=13.gif)
        ![Alt text](folder/image[14].bmp)
        ![Alt text](folder/image]15.jpeg)
        ![Alt text](folder/image{16}.png)
        ![Alt text](folder/image}17.jpg)
        ![Alt text](folder/image~18.gif)
        ![Alt text](folder/image!19.bmp)
        ![Alt text](folder/image%20.jpeg)
        """
        result = self.parser._get_media_references(markdown)
        expected = [
            'image_1.png', 'folder/image-2.jpg', 'folder/image.3.gif',
            'folder/image@4.bmp', 'folder/image#5.jpeg', 'folder/image$6.png',
            'folder/image&7.jpg', 'folder/image(8).gif', 'folder/image)9.bmp',
            'folder/image+10.jpeg', 'folder/image,11.png', 'folder/image;12.jpg',
            'folder/image=13.gif', 'folder/image[14].bmp', 'folder/image]15.jpeg',
            'folder/image{16}.png', 'folder/image}17.jpg', 'folder/image~18.gif',
            'folder/image!19.bmp', 'folder/image%20.jpeg'
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()


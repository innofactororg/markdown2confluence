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


if __name__ == '__main__':
    unittest.main()

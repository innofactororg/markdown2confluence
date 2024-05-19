import unittest
from unittest import mock
from markdown2confluence.publisher import ConfluencePublisher
from markdown2confluence.content_tree import ContentTree, ContentNode


class TestConfluencePublisher(unittest.TestCase):

    @mock.patch('markdown2confluence.publisher.ConfluenceClient')
    def setUp(self, MockConfluenceClient):
        self.mock_confluence_client = MockConfluenceClient.return_value
        self.mock_confluence_client.publish_page.return_value = 1234
        self.publisher = ConfluencePublisher(self.mock_confluence_client)

    @mock.patch('markdown2confluence.publisher.logger')
    def test_publish_content_handles_exception(self, mock_logger):
        # Create a minimal content tree with one node
        root_node = ContentNode(name='root')
        content_tree = ContentTree(root=root_node)

        # Simulate an exception when publishing a page
        self.mock_confluence_client.publish_page.side_effect = Exception(
            "Error")

        # Run the method
        self.publisher.publish_content(content_tree)

        # Check that the error was logged
        mock_logger.error.assert_called_with(
            'Failed to publish page %s: %s', 'root', 'Error')

    def test_publish_content_processes_children(self):
        # Create a content tree with root and one child node
        child_node = ContentNode(
            name='child',
            content='some content',
            metadata={'dummy': 'child metadata'}
        )
        root_node = ContentNode(
            name='root',
            children={'child': child_node},
            metadata={'dummy': 'root metadata'}
        )
        content_tree = ContentTree(root=root_node)

        # Run the method
        self.publisher.publish_content(content_tree)

        calls = [
            mock.call(
                title='root',
                content='',
                parent_id=None,
                metadata={'dummy': 'root metadata'},
            ),
            mock.call(
                title='child',
                content='some content',
                parent_id=1234,
                metadata={'dummy': 'child metadata'},
            )
        ]
        self.mock_confluence_client.publish_page.assert_has_calls(
            calls, any_order=True)

    @mock.patch('markdown2confluence.publisher.logger')
    def test_publish_content_logs_node_processing(self, mock_logger):
        # Create a minimal content tree with one node
        root_node = ContentNode(name='root')
        content_tree = ContentTree(root=root_node)

        # Run the method
        self.publisher.publish_content(content_tree)

        # Check that processing the node was logged
        mock_logger.debug.assert_any_call('Processing node: %s', 'root')


if __name__ == '__main__':
    unittest.main()

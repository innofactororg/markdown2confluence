import unittest
from unittest import mock
from markdown2confluence.publisher import Publisher
from markdown2confluence.config import Config
from markdown2confluence.content_tree import ContentTree, ContentNode


# Create a mock publisher inheriting from Publisher to test abstract methods
class MockPublisher(Publisher):
    def publish_node(self, node, parent_id):
        return ''


class TestPublisher(unittest.TestCase):
    def setUp(self):
        self.publisher = MockPublisher(config=Config.__new__(Config))
        self.publisher.config.confluence_root_page = None
        self.publisher.config.confluence_parent_page_id = 'mock_parent_id'

        self.mock_publish_node = mock.patch.object(
            MockPublisher, 'publish_node', autospec=True
        ).start()
        self.mock_publish_node.side_effect = (
            lambda __self__, node, __parent_id__: f"mock_id_for_{node.name}"
        )
        self.addCleanup(mock.patch.stopall)

    def test_publish_nested(self):
        self.publisher.config.confluence_root_page = ''

        # Create a simple content tree
        root = ContentNode(name='root')
        child1 = ContentNode(name='child1')
        child2 = ContentNode(name='child2')
        child3 = ContentNode(name='child3')
        root.add_child(child1)
        root.add_child(child2)
        child2.add_child(child3)
        content_tree = ContentTree(root=root)

        # Call publish_content
        self.publisher.publish_content(content_tree)

        self.assertEqual(self.mock_publish_node.call_count, 3)
        self.mock_publish_node.assert_any_call(
            self.publisher, child1, None
        )
        self.mock_publish_node.assert_any_call(
            self.publisher, child2, None
        )
        self.mock_publish_node.assert_any_call(
            self.publisher, child3, 'mock_id_for_child2'
        )

    def test_publish_root_page(self):
        self.publisher.config.confluence_root_page = 'rootpagename'

        # Create a simple content tree
        root = ContentNode(name='root')
        child1 = ContentNode(name='child1')
        child2 = ContentNode(name='child2')
        root.add_child(child1)
        root.add_child(child2)
        content_tree = ContentTree(root=root)

        # Call publish_content
        self.publisher.publish_content(content_tree)

        self.assertEqual(self.mock_publish_node.call_count, 3)
        self.mock_publish_node.assert_any_call(
            self.publisher, root, 'mock_parent_id'
        )
        self.mock_publish_node.assert_any_call(
            self.publisher, child1, 'mock_id_for_rootpagename'
        )
        self.mock_publish_node.assert_any_call(
            self.publisher, child2, 'mock_id_for_rootpagename'
        )

    def test_publish_with_circular_reference(self):
        # Create nodes with circular references
        node_a = ContentNode(name='A')
        node_b = ContentNode(name='B')
        node_a.add_child(node_b)
        node_b.add_child(node_a)
        content_tree = ContentTree(root=node_a)

        with self.assertRaises(RuntimeError):
            self.publisher.publish_content(content_tree)

    def test_publish_with_missing_root(self):
        # Create a content tree without a root
        content_tree = ContentTree(root=None)

        with self.assertRaises(AttributeError):
            self.publisher.publish_content(content_tree)

    def test_publish_with_none_node(self):
        # Create a content tree with a None node
        content_tree = ContentTree(root=None)

        with self.assertRaises(AttributeError):
            self.publisher.publish_content(content_tree)

    def test_pre_post_hooks_called(self):
        self.publisher.pre_publish_hook = mock.MagicMock()
        self.publisher.post_publish_hook = mock.MagicMock()

        # Create a simple content tree
        root = ContentNode(name='root')
        content_tree = ContentTree(root=root)

        # Call publish_content
        self.publisher.publish_content(content_tree)

        self.publisher.pre_publish_hook.assert_called_once()
        self.publisher.post_publish_hook.assert_called_once()


if __name__ == '__main__':
    unittest.main()

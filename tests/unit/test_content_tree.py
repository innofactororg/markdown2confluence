import unittest
from markdown2confluence.content_tree import ContentNode, ContentTree


class TestContentNode(unittest.TestCase):
    def setUp(self):
        self.root = ContentNode(name='root')
        self.child1 = ContentNode(name='child1', parent=self.root)
        self.child2 = ContentNode(name='child2', parent=self.root)
        self.root.add_child(self.child1)
        self.root.add_child(self.child2)

    def test_add_child(self):
        self.assertIn('child1', self.root.children)
        self.assertIn('child2', self.root.children)

    def test_get_child(self):
        self.assertEqual(self.root.get_child('child1'), self.child1)
        self.assertIsNone(self.root.get_child('nonexistent'))

    def test_is_leaf(self):
        self.assertFalse(self.root.is_leaf())
        self.assertTrue(self.child1.is_leaf())

    def test_is_root(self):
        self.assertTrue(self.root.is_root())
        self.assertFalse(self.child1.is_root())

    def test_str(self):
        expected = "'root'\n\t'child1'\n\t'child2'\n"
        self.assertEqual(str(self.root), expected)


class TestContentTree(unittest.TestCase):
    def setUp(self):
        self.tree = ContentTree()

    def test_add_node(self):
        self.tree.add_node(['level1', 'level2'], content='test content')
        node = self.tree.find_node(['level1', 'level2'])
        self.assertIsNotNone(node)
        self.assertEqual(node.content, 'test content')

    def test_find_node(self):
        self.tree.add_node(['level1', 'level2a'])
        self.tree.add_node(['level1', 'level2b'])
        node_a = self.tree.find_node(['level1', 'level2a'])
        node_b = self.tree.find_node(['level1', 'level2b'])
        self.assertIsNotNone(node_a)
        self.assertIsNotNone(node_b)
        self.assertIsNone(self.tree.find_node(['nonexistent']))

    def test_tree_str(self):
        self.tree.add_node(['level1', 'level2'], content='test content')
        expected = "'root'\n\t'level1'\n\t\t'level2'\n"
        self.assertEqual(str(self.tree), expected)

    def test_add_node_nested(self):
        self.tree.add_node(['level1', 'level2', 'level3'], content='nested')
        node = self.tree.find_node(['level1', 'level2', 'level3'])
        self.assertIsNotNone(node)
        self.assertEqual(node.content, 'nested')

    def test_add_node_empty_parent(self):
        with self.assertRaises(ValueError):
            self.tree.add_node(['', 'level1'])

    def test_find_node_invalid(self):
        self.assertIsNone(self.tree.find_node(['level1', 'nonexistent']))

    def test_multiple_children(self):
        self.tree.add_node(['level1', 'child1'])
        self.tree.add_node(['level1', 'child2'])
        node1 = self.tree.find_node(['level1', 'child1'])
        node2 = self.tree.find_node(['level1', 'child2'])
        self.assertIsNotNone(node1)
        self.assertIsNotNone(node2)

    def test_add_same_node_twice(self):
        self.tree.add_node(['level1', 'level2'], content='first')
        self.tree.add_node(['level1', 'level2'], content='second')
        node = self.tree.find_node(['level1', 'level2'])
        self.assertEqual(node.content, 'second')

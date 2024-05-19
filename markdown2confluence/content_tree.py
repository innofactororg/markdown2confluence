from dataclasses import dataclass, field


@dataclass
class ContentNode:
    name: str
    content: str | None = None
    metadata: dict | None = None
    parent: 'ContentNode | None' = None
    children: dict[str, 'ContentNode'] = field(default_factory=dict)

    def add_child(self, node: 'ContentNode'):
        self.children[node.name] = node

    def get_child(self, name: str) -> 'ContentNode | None':
        return self.children.get(name)

    def is_leaf(self) -> bool:
        return not self.children

    def __str__(self, level: int = 0) -> str:
        ret = "\t" * level + repr(self.name) + "\n"
        for child in self.children.values():
            ret += child.__str__(level + 1)
        return ret


@dataclass
class ContentTree:
    root: ContentNode = field(default_factory=lambda: ContentNode('root'))

    # Example usage:
    # ContentTree().add_node(
    #   path_list=['folder1', 'folder2', 'file.md'],
    #   content='file content here',
    #   metadata={'date': '2023-04-01'}
    # )
    def add_node(self, path_list: list, content: str | None = None,
                 metadata: dict | None = None):
        current_node = self.root
        for part in path_list:
            next_node = current_node.get_child(part)
            if not next_node:
                next_node = ContentNode(name=part, parent=current_node)
                current_node.add_child(next_node)
            current_node = next_node
        current_node.content = content
        current_node.metadata = metadata

    def find_node(self, path_list: list) -> ContentNode | None:
        current_node = self.root
        for part in path_list:
            current_node = current_node.get_child(part)
            if current_node is None:
                return None
        return current_node

    def __str__(self) -> str:
        return str(self.root)

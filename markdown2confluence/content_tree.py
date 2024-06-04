from dataclasses import dataclass, field


@dataclass
class ContentNode:
    name: str
    content: str | None = None
    metadata: dict | None = None
    parent: 'ContentNode | None' = None
    children: dict[str, 'ContentNode'] = field(default_factory=dict)

    def add_child(self, node: 'ContentNode'):
        node.parent = self
        self.children[node.name] = node

    def get_child(self, name: str) -> 'ContentNode | None':
        return self.children.get(name)

    def is_leaf(self) -> bool:
        return not self.children

    def is_root(self) -> bool:
        return self.parent is None

    def _set_name(self, name: str):
        self.name = name
        return

    def __str__(self, level: int = 0) -> str:
        ret = "\t" * level + repr(self.name) + "\n"
        for child in self.children.values():
            ret += child.__str__(level + 1)
        return ret


@dataclass
class ContentTree:
    root: ContentNode = field(default_factory=lambda: ContentNode('root'))

    def add_node(self, path_list: list, content: str | None = None,
                 metadata: dict | None = None):
        if not path_list:
            raise ValueError("Path list cannot be empty.")
        current_node = self.root
        for part in path_list:
            if not part:
                raise ValueError("Path components must be non-empty strings.")
            next_node = current_node.get_child(part)
            if not next_node:
                next_node = ContentNode(name=part)
                current_node.add_child(next_node)
            current_node = next_node
        if current_node is self.root:
            raise ValueError("Cannot add content to the root node.")
        current_node.content = content
        current_node.metadata = metadata

    def find_node(self, path_list: list) -> ContentNode | None:
        if not path_list:
            raise ValueError("Path list cannot be empty.")
        current_node = self.root
        for part in path_list:
            if not part:
                raise ValueError("Path components must be non-empty strings.")
            current_node = current_node.get_child(part)
            if current_node is None:
                return None
        return current_node

    def rename_root(self, name: str):
        self.root._set_name(name)

    def __str__(self) -> str:
        return str(self.root)

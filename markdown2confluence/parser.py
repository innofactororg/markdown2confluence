import os

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from collections.abc import Iterator


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


class Parser(ABC):
    @abstractmethod
    def parse_directory(self, directory: str) -> ContentTree:
        pass


class MarkdownParser(Parser):

    def parse_directory(self, directory: str) -> ContentTree:
        content_tree = ContentTree()
        for file_path in self._get_markdown_files(directory):
            content = self._read_file_content(file_path)
            path_list = self._get_relative_path_as_list(file_path, directory)
            content_tree.add_node(path_list=path_list, content=content)
        return content_tree

    def _get_markdown_files(self, directory: str) -> Iterator[str]:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    yield os.path.join(root, file)

    def _read_file_content(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} was not found.")
        with open(file_path, 'r', encoding='utf-8') as md_file:
            return md_file.read()

    def _get_relative_path_as_list(
            self, file_path: str, base_directory: str) -> list[str]:
        return os.path.relpath(file_path, base_directory).split(os.sep)

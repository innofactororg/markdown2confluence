import os

from abc import ABC, abstractmethod
from collections.abc import Iterator

from markdown2confluence.content_tree import ContentTree


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

import os
import re

from abc import ABC, abstractmethod
from collections.abc import Iterator

from markdown2confluence.util import Logger
from markdown2confluence.content_tree import ContentTree

logger = Logger(__name__).get_logger()


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
            attachments = self._get_media_references(content)

            content_tree.add_node(
                path_list=path_list,
                content=content,
                metadata={'attachments': attachments}
            )
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

    def _get_media_references(self, markdown: str) -> list[str]:
        files_to_upload = []

        for line in markdown.splitlines():
            match = re.search(
                r"!\[.*?\]\((?!http)(.*?\.(?:jpg|jpeg|png|gif|bmp|svg|webp|tiff))\)",  # noqa E501
                line
            )
            if match:
                file_path = match.group(1)
                logger.debug(f"Found file for attaching: {file_path}")
                files_to_upload.append(file_path)

        return files_to_upload

    def _get_relative_path_as_list(
            self, file_path: str, base_directory: str) -> list[str]:
        return os.path.relpath(file_path, base_directory).split(os.sep)

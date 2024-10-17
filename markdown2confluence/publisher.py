from abc import ABC, abstractmethod

from markdown2confluence.util import Logger
from markdown2confluence.config import Config
from markdown2confluence.content_tree import ContentTree, ContentNode

logger = Logger(__name__).get_logger()


class Publisher(ABC):
    def __init__(self, config: Config | None = None):
        self.config = config if config is not None else Config()

    @abstractmethod
    def publish_node(self, node: ContentNode, parent_id: str | None) -> str:
        pass

    def pre_publish_hook(self):
        """
        Optional step for actions to perform before publishing, such as
        fetching/deleting previously published resources.
        Can be overridden by subclasses.
        """
        pass

    def post_publish_hook(self):
        """
        Optional step for actions to perform after publishing, such as
        cleaning up resources or performing additional logging.
        Can be overridden by subclasses.
        """
        pass

    def publish_content(self, content_tree: ContentTree):
        logger.debug("ContentTree:\n%s", content_tree)

        root_page = self.config.confluence_root_page
        if root_page:
            content_tree.rename_root(root_page)

        self.pre_publish_hook()

        def traverse_and_publish(
                node: ContentNode,
                parent_id: str | None = None):
            logger.debug("Processing node: %s", node.name)

            if node.is_root():
                root_page = self.config.confluence_root_page
                if root_page not in (None, ''):
                    parent_id = self.publish_node(
                        node, self.config.confluence_parent_page_id)
            else:
                parent_id = self.publish_node(node, parent_id)

            for child in node.children.values():
                traverse_and_publish(child, parent_id)

        traverse_and_publish(content_tree.root)

        self.post_publish_hook()

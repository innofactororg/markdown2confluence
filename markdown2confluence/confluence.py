from atlassian import Confluence

from markdown2confluence.util import Logger
from markdown2confluence.config import Config
from markdown2confluence.publisher import Publisher
from markdown2confluence.content_tree import ContentNode


logger = Logger(__name__).get_logger()


class ConfluencePublisher(Publisher):
    def __init__(self, confluence: Confluence | None = None):
        self.config = Config()
        self.confluence = confluence or Confluence(
            url=self.config.confluence_url,
            username=self.config.confluence_username,
            password=self.config.confluence_password,
            cloud=True)
        logger.info("Initialized Publisher")

    def publish_node(self, node: ContentNode, parent_id: str | None) -> str:
        title = f"{node.name}"
        content = node.content if node.content else ""
        parent_page = int(parent_id) if parent_id is not None else None

        try:
            page_id = self.confluence.publish_page(
                title=title,
                content=content,
                parent_id=parent_page,
                metadata=node.metadata
            )
            return str(page_id)
        except Exception as e:
            logger.error("Failed to publish page %s: %s", title, str(e))
            return ''

from markdown2confluence.config import Config
from markdown2confluence.util import Logger
from markdown2confluence.confluence import ConfluenceClient
from markdown2confluence.parser import MarkdownParser as Parser

config = Config()
logger = Logger(__name__).get_logger()


class Publisher:
    def __init__(self, confluence: ConfluenceClient | None = None):
        self.confluence = confluence or ConfluenceClient(
            confluence_config=config.confluence
        )
        logger.info("Initialized Publisher")

    def publish_directory(self, directory: str):
        parser = Parser()
        content_tree = parser.parse_directory(directory)
        logger.debug("ContentTree:\n%s", content_tree)

        # TODO: traverse tree and publish with ConfluenceClient.publish_page

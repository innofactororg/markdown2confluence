from markdown2confluence.config import Config
from markdown2confluence.util import Logger
from markdown2confluence.confluence import ConfluenceClient

config = Config()
logger = Logger(__name__).get_logger()


class Publisher:
    def __init__(self, confluence: ConfluenceClient = None):
        self.confluence = confluence or ConfluenceClient(
            confluence_config=config.confluence
        )
        logger.info("Initialized Publisher")

    def publish_folder(self, folder_path: str):
        pass

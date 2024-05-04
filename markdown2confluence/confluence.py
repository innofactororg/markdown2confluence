from markdown2confluence.util import Logger

logger = Logger(__name__).get_logger()


class ConfluenceClient:
    def __init__(self, confluence_config: dict):
        self.api_endpoint = confluence_config["url"]
        self.auth = (confluence_config["username"],
                     confluence_config["password"])

    def create_or_update_page(self, title: str, content: str, parent_id=None):
        pass

    def delete_page(self, page_id: str):
        pass

    def publish_page(self, title: str, content: str, attachments: list[str]):
        pass

    def attach_file(self, page_id: int, attached_file: str):
        pass

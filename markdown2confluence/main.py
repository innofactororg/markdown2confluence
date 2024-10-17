from markdown2confluence.confluence import ConfluencePublisher as Publisher
from markdown2confluence.parser import MarkdownParser as Parser
from markdown2confluence.logo import LOGO_TEXT
from markdown2confluence.util import Logger
from markdown2confluence.config import Config

import importlib.metadata

logger = Logger("main").get_logger()
version = importlib.metadata.version("markdown2confluence")


def logo_and_version():
    logger.info(LOGO_TEXT)


def main():
    logo_and_version()
    logger.info(f"Started markdown2confluence version: {version}")

    config = Config()
    directory = config.markdown_folder

    logger.info("Parsing folder %s", directory)
    content = Parser().parse_directory(directory)

    logger.info("Publishing content from directory %s", directory)
    Publisher().publish_content(content)


if __name__ == "__main__":
    main()

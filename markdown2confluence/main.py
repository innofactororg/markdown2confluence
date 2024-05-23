from markdown2confluence.confluence import ConfluencePublisher as Publisher
from markdown2confluence.parser import MarkdownParser as Parser
from markdown2confluence.logo import LOGO_TEXT
from markdown2confluence.util import Logger
from markdown2confluence.config import Config

import importlib.metadata

config = Config()
logger = Logger("main").get_logger()


def logo_and_version():
    print(LOGO_TEXT)
    version = importlib.metadata.version("markdown2confluence")
    print(f"Version: {version}\n")


def main():
    logo_and_version()
    logger.info("Started markdown2confluence")

    directory = config.markdown_folder

    logger.info("Parsing folder %s", directory)
    content = Parser().parse_directory(directory)

    logger.info("Publishing content from directory %s", directory)
    Publisher().publish_content(content)


if __name__ == "__main__":
    main()

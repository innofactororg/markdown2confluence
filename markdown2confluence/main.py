from publisher import Publisher
from config import Config
from util import Logger
from logo import LOGO_TEXT
import pkg_resources

config = Config()
logger = Logger(__name__).get_logger()


def logo_and_version():
    print(LOGO_TEXT)
    version = pkg_resources.get_distribution("markdown2confluence").version
    print(f"Version: {version}\n")


def main():
    logo_and_version()
    logger.info("Started markdown2confluence")

    Publisher().publish_folder(config.markdown_folder)


if __name__ == "__main__":
    main()

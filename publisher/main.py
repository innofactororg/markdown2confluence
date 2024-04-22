import time
import logging

from config.get_config import get_config
from pages_controller import delete_pages, search_pages
from pages_publisher import publish_folder

config = get_config()
logging.basicConfig(level=logging.INFO)


def main():
    # Load configuration
    logging.debug(config)

    # Extract the arguments for easier access
    login = config["confluence_username"]
    password = config["confluence_password"]

    # Search and delete pages
    pages = search_pages(login=login, password=password)
    delete_pages(pages_id_list=pages, login=login, password=password)

    time.sleep(5)  # Sleep for 5 seconds to allow the delete to fully complete

    # Publish the markdown files from the specified folder
    publish_folder(
        folder=config["markdown_folder"], login=login, password=password
    )


if __name__ == '__main__':
    main()

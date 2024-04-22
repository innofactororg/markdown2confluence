import argparse
import logging

from config.get_config import get_config
from pages_controller import delete_pages, search_pages
from pages_publisher import publish_folder

logging.basicConfig(level=logging.INFO)


def main():
    # Parse arguments with LOGIN and PASSWORD for Confluence
    parser = argparse.ArgumentParser(
        description='Publish markdown files to Confluence.')
    parser.add_argument('--login', required=True,
                        help='Confluence login username.')
    parser.add_argument('--password', required=True,
                        help='Confluence login password.')
    args = parser.parse_args()

    # Extract the arguments for easier access
    login = args.login
    password = args.password

    # Load configuration
    config = get_config()
    logging.debug(config)

    # Search and delete pages
    pages = search_pages(login=login, password=password)
    delete_pages(pages_id_list=pages, login=login, password=password)

    # Publish the markdown files from the specified folder
    publish_folder(
        folder=config["github_folder_with_md_files"], login=login, password=password)


if __name__ == '__main__':
    main()


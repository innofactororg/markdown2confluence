import logging
import time

from config import Config
from converter import Converter
from publisher import Publisher


def main():
    config = Config()

    converter = Converter()
    publisher = Publisher(
        url=config.confluence_url,
        username=config.confluence_username,
        password=config.confluence_password,
        space_id=config.confluence_space_id,
        parent_page_id=config.confluence_parent_page_id,
        page_title_suffix=config.confluence_page_title_suffix,
        page_label=config.confluence_page_label,
        markdown_folder=config.markdown_folder,
        markdown_source_ref=config.markdown_source_ref,
        confluence_ignorefile=config.confluence_ignorefile)

    logging.basicConfig(level=logging.INFO)
    logging.debug(config)

    pages = publisher.search_pages()
    publisher.delete_pages(pages_id_list=pages)

    time.sleep(5)  # Sleep for 5 seconds to allow the delete to fully complete

    # Publish the markdown files from the specified folder
    publisher.publish_folder(
        folder=config.markdown_folder,
        parent_page_id=config.confluence_parent_page_id
    )


if __name__ == "__main__":
    main()

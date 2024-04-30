from converter import Converter
from publisher import Publisher
from config import Config


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
        page_label=config.confluence_page_label)

    # Implement logic to walk through the markdown-folder and convert/publish files
    # based on the specified confluence-search-pattern and ignore patterns from
    # confluence-ignorefile
    # ...
    # Example usage:
    # confluence_content = converter.convert(markdown_content)
    # publisher.publish(confluence_content, page_title)


if __name__ == "__main__":
    main()

from converter import Converter
from publisher import Publisher
from config import Config


def main():
    config = Config()

    converter = Converter()
    publisher = Publisher(
        config.confluence_username, config.confluence_password,
        config.confluence_url, config.confluence_space_id,
        config.confluence_parent_page_id)

    # Implement logic to walk through the markdown-folder and convert/publish files
    # based on the specified confluence-search-pattern and ignore patterns from
    # confluence-ignorefile
    # ...
    # Example usage:
    # confluence_content = converter.convert(markdown_content)
    # publisher.publish(confluence_content, page_title)


if __name__ == "__main__":
    main()

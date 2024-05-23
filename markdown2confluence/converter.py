import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from markdown.extensions.meta import MetaExtension
from markdown.extensions.toc import TocExtension


class Converter:
    """Converts Markdown files to HTML."""

    def __init__(self):
        """Initialize the converter."""
        pass

    @staticmethod
    def convert_markdown_to_html(markdown_content):
        """Convert Markdown content to HTML.

        Args:
            markdown_content (str): Markdown content to be converted.

        Returns:
            str: HTML content generated from the Markdown.
        """
        extensions = [
            CodeHiliteExtension(linenums=False, guess_lang=False),
            ExtraExtension(),
            MetaExtension(),
            TocExtension(permalink=True)
        ]
        html_content = markdown.markdown(
            markdown_content, extensions=extensions)
        return html_content


import markdown


class Converter:
    """Converts Markdown files to HTML."""

    def __init__(self):
        """Initialize the converter."""
        pass

    def convert_markdown_to_html(self, markdown_content):
        """Convert Markdown content to HTML.

        Args:
            markdown_content (str): Markdown content to be converted.

        Returns:
            str: HTML content generated from the Markdown.
        """
        html_content = markdown.markdown(markdown_content)
        return html_content

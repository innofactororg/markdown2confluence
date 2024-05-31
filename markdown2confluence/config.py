import argparse
import os

from markdown2confluence.util import Logger

logger = Logger(__name__).get_logger()


class Config:
    def __init__(self, args=None):
        if args is None:
            args = parse_args()

        self.confluence_url = (
            args.confluence_url or
            os.environ.get('CONFLUENCE_URL', '')
        ).rstrip('/')
        self.confluence_username = (
            args.confluence_username or
            os.environ.get('CONFLUENCE_USERNAME')
        )
        self.confluence_password = (
            args.confluence_password or
            os.environ.get('CONFLUENCE_PASSWORD')
        )
        self.confluence_space_id = (
            args.confluence_space_id or
            os.environ.get('CONFLUENCE_SPACE_ID')
        )
        self.confluence_parent_page_id = (
            args.confluence_parent_page_id or
            os.environ.get('CONFLUENCE_PARENT_PAGE_ID')
        )
        self.confluence_page_title_suffix = (
            args.confluence_page_title_suffix or
            os.environ.get('CONFLUENCE_PAGE_TITLE_SUFFIX') or
            '(autogenerated)'
        )
        self.confluence_page_label = (
            args.confluence_page_label or
            os.environ.get('CONFLUENCE_PAGE_LABEL') or
            'markdown2confluence'
        )

        self.markdown_folder = (
            args.markdown_folder or
            os.environ.get('MARKDOWN_FOLDER') or
            './'
        )
        self.markdown_source_ref = (
            args.markdown_source_ref or
            os.environ.get('MARKDOWN_SOURCE_REF')
        )
        self.confluence_ignorefile = (
            args.confluence_ignorefile or
            os.environ.get('CONFLUENCE_IGNOREFILE')
        )

        self.validate()

    def validate(self):
        missing_fields = []

        required_fields = ['confluence_url', 'confluence_username',
                           'confluence_password', 'confluence_space_id',
                           'confluence_parent_page_id',
                           'confluence_page_title_suffix']

        for key in required_fields:
            if not getattr(self, key):
                missing_fields.append(key)

        if missing_fields:
            raise ValueError("The following configuration fields are "
                             "missing or empty: " + ", ".join(missing_fields))


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Pushes a folder of Markdown files to Confluence, maintaining the "
            "page structure according to the file and folder hierarchy, while "
            "ignoring non-Markdown files."
        )
    )

    parser.add_argument(
        '--confluence-url',
        help="Confluence base URL")
    parser.add_argument(
        '--confluence-username',
        help="Confluence username")
    parser.add_argument(
        '--confluence-password',
        help="Confluence password")
    parser.add_argument(
        '--confluence-space-id',
        help="Confluence space key")
    parser.add_argument(
        '--confluence-parent-page-id',
        help="Parent page ID under which to add the new page")
    parser.add_argument(
        '--markdown-folder',
        help="File or folder containing Markdown files to publish")
    parser.add_argument(
        '--markdown-source-ref',
        help="Source reference of the Markdown, e.g. github.com/org/repo")
    parser.add_argument(
        '--confluence-ignorefile',
        help="Path to a file with patterns to ignore files or directories")
    parser.add_argument(
        '--confluence-page-title-suffix',
        help="Suffix for Confluence page titles, to denote pages "
             "managed by markdown2confluence")
    parser.add_argument(
        '--confluence-page-label',
        help=("Label to assign to Confluence pages managed by "
              "markdown2confluence"))

    return parser.parse_args()

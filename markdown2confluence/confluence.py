from markdown2confluence.api import MinimalConfluence as Confluence
import requests
import hashlib

from markdown2confluence.util import Logger
from markdown2confluence.config import Config
from markdown2confluence.converter import Converter
from markdown2confluence.publisher import Publisher
from markdown2confluence.content_tree import ContentNode


logger = Logger(__name__).get_logger()


class ConfluencePublisher(Publisher):
    def __init__(self, confluence: Confluence | None = None):
        self.config = Config()
        self.confluence = confluence or Confluence(
            url=self.config.confluence_url,
            username=self.config.confluence_username,
            password=self.config.confluence_password,
        )
        self.suffix = self.config.confluence_page_title_suffix
        self.label = self.config.confluence_page_label
        self.autogen_notice = (
            "<ac:structured-macro ac:name=\"note\" ac:schema-version=\"1\">"
            "<ac:parameter ac:name=\"title\">Do not make changes here</ac:parameter>"
            "<ac:rich-text-body>"
            "<p>This page is autogenerated. Make changes in the "
            f"<a href=\"{self.config.markdown_source_ref}\">GitHub repository</a></p>"
            "</ac:rich-text-body>"
            "</ac:structured-macro>"
        )

        logger.info("Initialized Publisher")

    def pre_publish_hook(self):
        cql = (
            f"space='{self.config.confluence_space_id}' "
            f"AND label='{self.label}' "
            f"AND title~'{self.suffix}'"
        )
        self.stale_pages: list[dict[str, any]] = self.confluence.search(
            cql).get('results', [])
        logger.info("Fetched %d stale pages", len(self.stale_pages))
        logger.debug("Stale pages: %s", self.stale_pages)

    def post_publish_hook(self):
        logger.debug(f"Found {len(self.stale_pages)} remaining stale pages")
        for page in self.stale_pages:
            page_id = page['id']
            title = page['title']

            if not title.endswith(self.suffix):
                logger.warning("Skipping deletion of unmanaged page %s", title)
                continue

            self.confluence.remove_page(page_id)
            logger.info("Deleted unmanaged page %s", title)

    def publish_node(self, node: ContentNode, parent_id: str | None) -> str:
        identifier = f"{node.name}{node.parent.name if node.parent else None}{self.config.confluence_root_page}"
        hash = hashlib.md5(identifier.encode('utf-8')).hexdigest()[:3]

        title = f"{node.name} #{hash} {self.suffix}"
        content = Converter.convert_markdown_to_html(node.content or "")
        content = self.autogen_notice + content
        parent_page = (
            int(parent_id) if parent_id is not None
            else self.config.confluence_parent_page_id
        )

        page = self._get_existing_page(title)
        if page and page['id']:
            logger.debug(
                f"Found existing page: {page['id']} matching title {title}")
            self._update_page(page['id'], title, content,
                              parent_page, node)
        else:
            logger.debug(
                f"Found no existing page for title {title}")
            page_id = self._create_page(title, content, parent_page, node)

        if node.metadata:
            self._attach_files(page_id, node.metadata.get('attachments', []))
        return str(page_id)

    def _get_existing_page(self, title: str) -> dict | None:
        for page in self.stale_pages:
            if page['title'] == title:
                self.stale_pages.remove(page)
                return page
        return None

    def _create_page(self, title: str, content: str, parent_id: int | None,
                     node: ContentNode) -> str:
        logger.debug(f"creating page {title} with parent id {parent_id}")
        try:
            page = self.confluence.create_page(
                space=self.config.confluence_space_id,
                title=title,
                body=content,
                parent_id=parent_id,
                type='page',
                representation='storage',
                editor='v2',
                full_width=False
            )
            page_id = str(page['id'])
            self.confluence.set_page_label(page_id, self.label)
            logger.info("Created page %s with ID %s", title, page_id)
            return page_id
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                logger.error("Error creating page: %s", e.response.text)
                raise ValueError(
                    "Failed to create page due to bad request.") from e
            else:
                logger.error("HTTP error occurred: %s", e.response.text)
                raise

    def _update_page(self, page_id: str, title: str, content: str,
                     parent_id: int | None, node: ContentNode):
        logger.debug(f"updating page {node.name} with parent {page_id}")
        try:
            page = self.confluence.get_page_by_id(page_id)
            version = int(page['version']['number'] +
                          1) if 'version' in page else 1
            print("page: ", page, "version: ", version)
            self.confluence.update_page(
                page_id=page_id,
                title=title,
                body=content,
                parent_id=parent_id,
                version=version,
            )
            self.confluence.set_page_label(page_id, self.label)
            logger.info("Updated page %s with ID %s and label %s",
                        title, page_id, self.label)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                logger.error("Error updating page: %s", e.response.text)
                raise ValueError(
                    "Failed to update page due to bad request.") from e
            else:
                logger.error("HTTP error occurred: %s", e.response.text)
                raise

    def _attach_files(self, page_id: str, attachments: list[dict]):
        for attachment in attachments:
            logger.debug(attachment)

            name = attachment['reference']
            filename = attachment['file_path']

            self.confluence.attach_file(
                filename=filename,
                name=name,
                page_id=page_id,
            )
            logger.info("Attached file %s with reference %s to page ID %s",
                        filename, name, page_id)

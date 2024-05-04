from atlassian import Confluence


class Publisher:
    def __init__(self, url, username, password, space_id,
                 parent_page_id, page_title_suffix,
                 page_label, markdown_folder,
                 markdown_source_ref, confluence_ignorefile):
        self.confluence = Confluence(
            url=url,
            username=username,
            password=password
        )
        self.space_id = space_id
        self.parent_page_id = parent_page_id
        self.page_title_suffix = page_title_suffix
        self.page_label = page_label
        self.markdown_folder = markdown_folder
        self.markdown_source_ref = markdown_source_ref

        # self.ignore_patterns = self.load_ignore_patterns(confluence_ignorefile)

    def publish_page(self, title, content):
        pass

    def update_page(self, page_id, title, content):
        pass

    def delete_page(self, page_id):
        pass

    def _attach_file(self, page_id, attached_file):
        pass

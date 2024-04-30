from atlassian import Confluence


class Publisher:
    def __init__(self, url, username, password, space_id,
                 parent_page_id, page_title_suffix, page_label):
        self.confluence = Confluence(
            url=url,
            username=username,
            password=password
        )
        self.space_id = space_id
        self.parent_page_id = parent_page_id
        self.page_title_suffix = page_title_suffix
        self.page_label = page_label

    def publish_page(self, title, content):
        title_with_suffix = f"{title}{self.page_title_suffix}"
        existing_page = self.confluence.get_page_by_title(
            space=self.space_id,
            title=title_with_suffix,
            expand='version'
        )
        if existing_page:
            return
            # return self.update_page(
            #     page_id=existing_page['id'],
            #     title=title_with_suffix,
            #     content=content
            # )
        else:
            return self.confluence.create_page(
                space=self.space_id,
                title=title_with_suffix,
                body=content,
                parent_id=self.parent_page_id,
                type='page'
            )

    def update_page(self, page_id, title, content):
        return self.confluence.update_page(
            page_id=page_id,
            title=title,
            body=content,
            type='page',
        )

    def delete_page(self, page_id):
        return self.confluence.remove_page(page_id)

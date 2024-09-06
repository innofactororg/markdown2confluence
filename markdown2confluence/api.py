import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class MinimalConfluence:
    def __init__(self, url: str, username: str, password: str):
        self.url = url if url.endswith('/') else url + '/'
        self.api = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.api.mount('https://', HTTPAdapter(max_retries=retries))

        if username and password:
            self.api.auth = HTTPBasicAuth(username, password)
        else:
            raise ValueError(
                'Both username and password (api token) must be set.')

    def _request(self, method: str, path: str, **kwargs):
        url = f'{self.url}{path}'
        response = self.api.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def _get(self, path: str, **kwargs):
        return self._request('GET', path, **kwargs)

    def _post(self, path: str, **kwargs):
        return self._request('POST', path, **kwargs)

    def _put(self, path: str, **kwargs):
        return self._request('PUT', path, **kwargs)

    def search(self, cql: str | None):
        # Add logic to perform a CQL search in Confluence
        pass

    def create_page(self, space: str, title: str, body: str,
                    parent_id: str | None):
        # Add logic to create a page in Confluence
        pass

    def update_page(self, page_id: str, title: str, body: str,
                    version: int | None):
        # Add logic to update a page in Confluence
        pass

    def remove_page(self, page_id: str | None):
        # Add logic to remove a page in Confluence
        pass

    def create_attachment(self, page_id: str, file_path: str,
                          comment: str | None):
        # Add logic to create an attachment in Confluence
        pass

    def get_attachments(self, page_id: str | None):
        # Add logic to get attachments from a page in Confluence
        pass

    def update_attachment(self, attachment_id: str, file_path: str,
                          comment: str | None):
        # Add logic to update an attachment in Confluence
        pass

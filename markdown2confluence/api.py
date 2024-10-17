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

        if response.status_code == 204:  # No Content
            return None

        return response.json()

    def _get(self, path: str, **kwargs):
        return self._request('GET', path, **kwargs)

    def _post(self, path: str, **kwargs):
        return self._request('POST', path, **kwargs)

    def _put(self, path: str, **kwargs):
        return self._request('PUT', path, **kwargs)

    def _del(self, path: str, **kwargs):
        return self._request('DELETE', path, **kwargs)

    def get_space_id_from_key(self, space_key: str) -> str:
        path = 'api/v2/spaces'
        response = self._get(path)
        if response is None:
            raise ValueError('Failed to retrieve spaces.')

        for space in response.get('results', []):
            if space.get('key') == space_key:
                return space.get('id')
        raise ValueError(f'Space key {space_key} not found.')

    def get_space_key_from_id(self, space_id: str) -> str:
        path = 'api/v2/spaces'
        response = self._get(path)
        if response is None:
            raise ValueError('Failed to retrieve spaces.')

        for space in response.get('results', []):
            if space.get('id') == space_id:
                return space.get('key')
        raise ValueError(f'Space ID {space_id} not found.')

    def search(self, cql: str):
        path = 'rest/api/content/search'
        params = {'cql': cql}
        return self._get(path, params=params)

    def get_page_by_id(self, page_id: str):
        path = f'rest/api/content/{page_id}'
        return self._get(path)

    def create_page(self, space: str, title: str, body: str,
                    parent_id: int | None):
        path = 'api/v2/pages'
        data = {
            'spaceId': '294916',  # space,
            'status': 'current',
            'title': title,
            'body': {
                'storage': {
                    'value': body,
                    'representation': 'storage'
                }
            }
        }
        if parent_id:
            data['parentId'] = parent_id
        return self._post(path, json=data)

    def update_page(self, page_id: str, title: str, parent_id: int | None,
                    body: str, version: int):
        path = f'rest/api/content/{page_id}'
        data = {
            'id': page_id,
            'status': 'current',
            'title': title,
            'type': 'page',
            'parentId': parent_id,
            'version': {'number': version},
            'body': {
                'storage': {
                    'value': body,
                    'representation': 'storage'
                }
            }
        }
        return self._put(path, json=data)

    def remove_page(self, page_id: str):
        path = f'api/v2/pages/{page_id}'
        return self._del(path)

    def create_or_update_attachment(self, page_id: str, file_path: str,
                                    comment: str | None = None):
        path = f'rest/api/content/{page_id}/child/attachment'
        files = {'file': open(file_path, 'rb')}
        params = {'comment': comment} if comment else {}
        return self._put(path, files=files, params=params)

    def get_attachments(self, page_id: str):
        path = f'api/v2/pages/{page_id}/attachments'
        return self._get(path)

    def update_attachment(self, attachment_id: str, file_path: str,
                          comment: str):
        path = f'rest/api/content/{attachment_id}/data'
        files = {'file': open(file_path, 'rb')}
        params = {'comment': comment} if comment else {}
        return self._post(path, files=files, params=params)

    def set_page_label(self, page_id: str, label: str):
        path = f'rest/api/content/{page_id}/label'
        data = {'prefix': 'global', 'name': label}
        return self._post(path, json=data)

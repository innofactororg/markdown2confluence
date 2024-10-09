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

    def search(self, cql: str):
        path = 'rest/api/content/search'
        params = {'cql': cql}
        return self._get(path, params=params)

    def get_page_by_id(self, page_id: str):
        path = f'rest/api/content/{page_id}'
        return self._get(path)

    def create_page(self, space: str, title: str, body: str,
                    parent_id: str):
        path = 'rest/api/content'
        data = {
            'type': 'page',
            'title': title,
            'space': {'key': space},
            'body': {
                'storage': {
                    'value': body,
                    'representation': 'storage'
                }
            }
        }
        if parent_id:
            data['ancestors'] = [{'id': parent_id}]
        return self._post(path, json=data)

    def update_page(self, page_id: str, title: str, parent_id: int,
                    body: str, version: int):
        path = f'rest/api/content/{page_id}'
        print("version is: ", version, type(version))
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
        path = f'rest/api/content/{page_id}'
        return self._request('DELETE', path)

    def create_attachment(self, page_id: str, file_path: str,
                          comment: str):
        path = f'rest/api/content/{page_id}/child/attachment'
        files = {'file': open(file_path, 'rb')}
        params = {'comment': comment} if comment else {}
        return self._post(path, files=files, params=params)

    def get_attachments(self, page_id: str):
        path = f'rest/api/content/{page_id}/child/attachment'
        return self._get(path)

    def update_attachment(self, attachment_id: str, file_path: str,
                          comment: str):
        path = f'rest/api/content/{attachment_id}/data'
        files = {'file': open(file_path, 'rb')}
        params = {'comment': comment} if comment else {}
        return self._post(path, files=files, params=params)

    # TODO: validate
    def set_page_label(self, page_id: str, label: str):
        path = f'rest/api/content/{page_id}/label'
        data = {'prefix': 'global', 'name': label}
        return self._post(path, json=data)

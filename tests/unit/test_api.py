import unittest
from unittest.mock import patch, MagicMock
from markdown2confluence.api import MinimalConfluence
from requests.exceptions import HTTPError


class TestMinimalConfluence(unittest.TestCase):

    def setUp(self):
        self.url = 'https://confluence.example.com'
        self.username = 'user'
        self.password = 'pass'
        self.confluence = MinimalConfluence(self.url, self.username, self.password)

    @patch('markdown2confluence.api.requests.Session.request')
    def test_request(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {'key': 'value'}
        self.assertEqual(
            self.confluence._request('GET', 'path'),
            {'key': 'value'}
        )

        mock_request.return_value.raise_for_status.side_effect = HTTPError
        with self.assertRaises(HTTPError):
            self.confluence._request('GET', 'path')

    @patch('markdown2confluence.api.requests.Session.request')
    def test_get(self, mock_request):
        self.confluence._get('path')
        mock_request.assert_called_with('GET', f'{self.url}/path')

    @patch('markdown2confluence.api.requests.Session.request')
    def test_post(self, mock_request):
        self.confluence._post('path')
        mock_request.assert_called_with('POST', f'{self.url}/path')

    @patch('markdown2confluence.api.requests.Session.request')
    def test_put(self, mock_request):
        self.confluence._put('path')
        mock_request.assert_called_with('PUT', f'{self.url}/path')

    @patch('markdown2confluence.api.requests.Session.request')
    def test_search(self, mock_request):
        # Since search is not implemented, we test for a NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.confluence.search('cql')

    @patch('markdown2confluence.api.requests.Session.request')
    def test_create_page(self, mock_request):
        # Since create_page is not implemented, we test for a NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.confluence.create_page(
                space='SPACE', title='Title', body='Body', parent_id=None
            )

    @patch('markdown2confluence.api.requests.Session.request')
    def test_update_page(self, mock_request):
        # Since update_page is not implemented, we test for a NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.confluence.update_page(page_id='123', title='Title', body='Body',
                                        version=None)

    @patch('markdown2confluence.api.requests.Session.request')
    def test_remove_page(self, mock_request):
        # Since remove_page is not implemented, we test for a NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.confluence.remove_page(page_id=None)

    @patch('markdown2confluence.api.requests.Session.request')
    def test_create_attachment(self, mock_request):
        # Since create_attachment is not implemented, we test for a NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.confluence.create_attachment(
                page_id='123', file_path='file.txt', comment=None
            )

    @patch('markdown2confluence.api.requests.Session.request')
    def test_get_attachments(self, mock_request):
        # Since get_attachments is not implemented, we test for a NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.confluence.get_attachments(page_id=None)

    @patch('markdown2confluence.api.requests.Session.request')
    def test_update_attachment(self, mock_request):
        # Since update_attachment is not implemented, we test for a NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.confluence.update_attachment(
                attachment_id='123', file_path='file.txt', comment=None
            )


if __name__ == '__main__':
    unittest.main()


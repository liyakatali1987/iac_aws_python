import unittest
from unittest.mock import patch # Removed MagicMock
import sys
import os

# Add the parent directory of 'atlassian_examples' to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # This is /tests
project_root = os.path.dirname(os.path.dirname(parent_dir)) # This is /
sys.path.insert(0, project_root)

from atlassian_examples.bitbucket.http_req import HttpRequests
# Removed: import requests 

class TestHttpRequests(unittest.TestCase):

    def test_init_default_headers_and_timeout(self):
        """Test HttpRequests.__init__ with default headers and timeout."""
        req = HttpRequests('get', 'http://test.com', 'user', 'pass')
        self.assertEqual(req.type, 'get')
        self.assertEqual(req.uri, 'http://test.com')
        self.assertEqual(req.user, 'user')
        self.assertEqual(req.pwrd, 'pass')
        self.assertIsNone(req.data)
        self.assertEqual(req.headers, {'Accept': 'application/json', 'Content-Type': 'application/json'})
        self.assertIsNone(req.params)
        self.assertEqual(req.timeout, 30) # Default timeout

    def test_init_custom_headers_and_timeout(self):
        """Test HttpRequests.__init__ with custom headers and timeout."""
        custom_headers = {'X-Custom-Header': 'Value', 'Accept': 'application/xml'}
        req = HttpRequests('post', 'http://test.com/api', 'admin', 'secret',
                           data='{"key":"val"}', headers=custom_headers,
                           params={'page': 1}, timeout=60)
        self.assertEqual(req.data, '{"key":"val"}')
        expected_headers = {'Accept': 'application/xml', # Overridden
                            'Content-Type': 'application/json', # Default
                            'X-Custom-Header': 'Value'}    # Custom
        self.assertEqual(req.headers, expected_headers)
        self.assertEqual(req.params, {'page': 1})
        self.assertEqual(req.timeout, 60)

    @patch('requests.get')
    def test_http_requests_get(self, mock_requests_get):
        """Test http_requests method for GET."""
        uri = 'http://test.com/get_resource'
        headers = {'X-Test': 'GET'}
        params = {'id': '123'}
        auth = ('test_user', 'test_pass')
        timeout = 45

        req = HttpRequests('get', uri, auth[0], auth[1], headers=headers, params=params, timeout=timeout)
        req.http_requests()

        mock_requests_get.assert_called_once_with(uri, headers=req.headers, params=params, auth=auth, timeout=timeout)

    @patch('requests.post')
    def test_http_requests_post(self, mock_requests_post):
        """Test http_requests method for POST."""
        uri = 'http://test.com/create_resource'
        data = '{"name": "new_item"}'
        headers = {'X-Test': 'POST'}
        auth = ('test_user', 'test_pass')
        timeout = 15

        req = HttpRequests('post', uri, auth[0], auth[1], data=data, headers=headers, timeout=timeout)
        req.http_requests()

        mock_requests_post.assert_called_once_with(uri, data=data, headers=req.headers, params=None, auth=auth, timeout=timeout)

    @patch('requests.put')
    def test_http_requests_put(self, mock_requests_put):
        """Test http_requests method for PUT."""
        uri = 'http://test.com/update_resource/1'
        data = '{"name": "updated_item"}'
        auth = ('test_user', 'test_pass')
        req = HttpRequests('put', uri, auth[0], auth[1], data=data)
        req.http_requests()

        mock_requests_put.assert_called_once_with(uri, data=data, headers=req.headers, params=None, auth=auth, timeout=req.timeout)

    @patch('requests.delete')
    def test_http_requests_delete(self, mock_requests_delete):
        """Test http_requests method for DELETE."""
        uri = 'http://test.com/delete_resource/1'
        auth = ('test_user', 'test_pass')

        # Note: data is intentionally not passed for DELETE as per previous subtask modifications
        req = HttpRequests('delete', uri, auth[0], auth[1])
        req.http_requests()

        mock_requests_delete.assert_called_once_with(uri, headers=req.headers, params=None, auth=auth, timeout=req.timeout)

if __name__ == '__main__':
    unittest.main()

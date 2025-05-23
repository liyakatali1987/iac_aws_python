import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory of 'atlassian_examples' to the Python path
# This is to ensure that the module 'atlassian_examples.bitbucket.bitbucket_client' can be found
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # This is /tests
project_root = os.path.dirname(os.path.dirname(parent_dir)) # This is /
sys.path.insert(0, project_root)

from atlassian_examples.bitbucket.bitbucket_client import BitbucketApi
from atlassian_examples.bitbucket.http_req import HttpRequests # Needed for mocking HttpRequests

class TestBitbucketApi(unittest.TestCase):

    def test_init(self):
        """Test BitbucketApi.__init__"""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        
        client = BitbucketApi(host, user, password)
        
        expected_base_api_url = f"{host}/rest/api/latest"
        expected_base_default_reviewers_url = f"{host}/rest/default-reviewers/latest"
        
        self.assertEqual(client.base_api_url, expected_base_api_url)
        self.assertEqual(client.base_default_reviewers_url, expected_base_default_reviewers_url)
        self.assertEqual(client.user, user)
        self.assertEqual(client.password, password)

    @patch.object(BitbucketApi, 'bitbucket_requests')
    def test_get_user_details_found(self, mock_bitbucket_requests):
        """Test get_user_details when user is found."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)
        
        user_id_to_find = "jdoe"
        mock_response_data = {
            "values": [
                {"name": "jdoe", "emailAddress": "jdoe@example.com", "id": 101},
                {"name": "asmith", "emailAddress": "asmith@example.com", "id": 102}
            ]
        }
        mock_bitbucket_requests.return_value = (200, mock_response_data, None)
        
        expected_user_details = {"name": "jdoe", "emailAddress": "jdoe@example.com", "id": 101}
        
        actual_user_details = client.get_user_details(user_id_to_find)
        
        mock_bitbucket_requests.assert_called_once_with('get', f"{client.base_api_url}/admin/users?filter={user_id_to_find}")
        self.assertEqual(actual_user_details, expected_user_details)

    @patch.object(BitbucketApi, 'bitbucket_requests')
    def test_get_user_details_not_found(self, mock_bitbucket_requests):
        """Test get_user_details when user is not found."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)
        
        user_id_to_find = "unknownuser"
        mock_response_data = {"values": []} # Empty list
        mock_bitbucket_requests.return_value = (200, mock_response_data, None)
        
        actual_user_details = client.get_user_details(user_id_to_find)
        
        mock_bitbucket_requests.assert_called_once_with('get', f"{client.base_api_url}/admin/users?filter={user_id_to_find}")
        self.assertIsNone(actual_user_details)

    @patch.object(BitbucketApi, 'bitbucket_requests')
    def test_get_user_details_not_found_in_list(self, mock_bitbucket_requests):
        """Test get_user_details when user is not in the returned list."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)
        
        user_id_to_find = "unknownuser"
        mock_response_data = {
            "values": [
                {"name": "jdoe", "emailAddress": "jdoe@example.com", "id": 101}
            ]
        }
        mock_bitbucket_requests.return_value = (200, mock_response_data, None)

        actual_user_details = client.get_user_details(user_id_to_find)

        mock_bitbucket_requests.assert_called_once_with('get', f"{client.base_api_url}/admin/users?filter={user_id_to_find}")
        self.assertIsNone(actual_user_details)

    @patch.object(BitbucketApi, 'bitbucket_requests')
    def test_get_user_details_api_error(self, mock_bitbucket_requests):
        """Test get_user_details when API returns an error."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)
        
        user_id_to_find = "jdoe"
        # Simulate an API error (e.g., bitbucket_requests returns an error)
        mock_bitbucket_requests.return_value = (500, "Internal Server Error", "Some error object or message")
        
        actual_user_details = client.get_user_details(user_id_to_find)
        
        mock_bitbucket_requests.assert_called_once_with('get', f"{client.base_api_url}/admin/users?filter={user_id_to_find}")
        self.assertIsNone(actual_user_details)

    @patch.object(BitbucketApi, 'bitbucket_requests')
    def test_get_user_details_no_values_key(self, mock_bitbucket_requests):
        """Test get_user_details when 'values' key is missing in response."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)
        
        user_id_to_find = "jdoe"
        mock_response_data = {} # Missing 'values' key
        mock_bitbucket_requests.return_value = (200, mock_response_data, None)
        
        actual_user_details = client.get_user_details(user_id_to_find)
        
        mock_bitbucket_requests.assert_called_once_with('get', f"{client.base_api_url}/admin/users?filter={user_id_to_find}")
        self.assertIsNone(actual_user_details)

    @patch.object(BitbucketApi, 'bitbucket_requests')
    def test_generic_add_default_reviewers_condition_project_success(self, mock_bitbucket_requests):
        """Test generic_add_default_reviewers_condition for project-level success."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)

        project_key = "TESTPROJ"
        users_details_list = [{"name": "jdoe", "id": 101}]
        reviewers_payload_config = {
            "sourceMatcher": {"id": "refs/heads/**"},
            "targetMatcher": {"id": "refs/heads/develop"},
            "requiredApprovals": 1
        }
        expected_url = f"{client.base_default_reviewers_url}/projects/{project_key}/condition"
        expected_data_payload = {
            "reviewers": users_details_list,
            "sourceMatcher": reviewers_payload_config["sourceMatcher"],
            "targetMatcher": reviewers_payload_config["targetMatcher"],
            "requiredApprovals": reviewers_payload_config["requiredApprovals"]
        }
        mock_bitbucket_requests.return_value = (201, {"message": "Created"}, None)

        status, response, error = client.generic_add_default_reviewers_condition(
            project_key, users_details_list, reviewers_payload_config
        )

        mock_bitbucket_requests.assert_called_once_with('post', expected_url, data=expected_data_payload)
        self.assertEqual(status, 201)
        self.assertEqual(response, {"message": "Created"})
        self.assertIsNone(error)

    @patch.object(BitbucketApi, 'bitbucket_requests')
    def test_generic_add_default_reviewers_condition_repo_success(self, mock_bitbucket_requests):
        """Test generic_add_default_reviewers_condition for repository-level success."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)

        project_key = "TESTPROJ"
        repo_name = "test-repo"
        users_details_list = [{"name": "jdoe", "id": 101}]
        reviewers_payload_config = {
            "sourceMatcher": {"id": "refs/heads/master"},
            "targetMatcher": {"id": "refs/heads/develop"},
            "requiredApprovals": 2
        }
        expected_url = f"{client.base_default_reviewers_url}/projects/{project_key}/repos/{repo_name}/condition"
        expected_data_payload = {
            "reviewers": users_details_list,
            "sourceMatcher": reviewers_payload_config["sourceMatcher"],
            "targetMatcher": reviewers_payload_config["targetMatcher"],
            "requiredApprovals": reviewers_payload_config["requiredApprovals"]
        }
        mock_bitbucket_requests.return_value = (200, {"message": "OK"}, None)

        status, response, error = client.generic_add_default_reviewers_condition(
            project_key, users_details_list, reviewers_payload_config, repo_name=repo_name
        )

        mock_bitbucket_requests.assert_called_once_with('post', expected_url, data=expected_data_payload)
        self.assertEqual(status, 200)
        self.assertEqual(response, {"message": "OK"})
        self.assertIsNone(error)

    @patch.object(BitbucketApi, 'bitbucket_requests')
    def test_generic_add_default_reviewers_condition_api_error(self, mock_bitbucket_requests):
        """Test generic_add_default_reviewers_condition when API returns an error."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)

        project_key = "TESTPROJ"
        users_details_list = [{"name": "jdoe", "id": 101}]
        reviewers_payload_config = {"sourceMatcher": {}, "targetMatcher": {}, "requiredApprovals": 1}
        
        mock_bitbucket_requests.return_value = (400, {"error": "Bad Request"}, "API Error")

        status, response, error = client.generic_add_default_reviewers_condition(
            project_key, users_details_list, reviewers_payload_config
        )
        
        self.assertEqual(status, 400)
        self.assertEqual(response, {"error": "Bad Request"})
        self.assertEqual(error, "API Error")

    @patch('atlassian_examples.bitbucket.bitbucket_client.HttpRequests')
    def test_bitbucket_requests_success_json_response(self, MockHttpRequests):
        """Test bitbucket_requests for a successful GET request with JSON response."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)

        mock_http_response = MagicMock()
        mock_http_response.status_code = 200
        mock_http_response.text = '{"key": "value"}'
        mock_http_response.json.return_value = {"key": "value"}
        
        # Configure the HttpRequests instance returned by the constructor
        mock_http_instance = MockHttpRequests.return_value
        mock_http_instance.http_requests.return_value = mock_http_response

        status, data, error = client.bitbucket_requests('get', f"{client.base_api_url}/some/endpoint")

        MockHttpRequests.assert_called_once_with('get', f"{client.base_api_url}/some/endpoint", client.user, client.password, data='null', params=None)
        mock_http_instance.http_requests.assert_called_once()
        self.assertEqual(status, 200)
        self.assertEqual(data, {"key": "value"})
        self.assertIsNone(error)

    @patch('atlassian_examples.bitbucket.bitbucket_client.HttpRequests')
    def test_bitbucket_requests_success_no_response_text(self, MockHttpRequests):
        """Test bitbucket_requests for a successful POST with no response text."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)

        mock_http_response = MagicMock()
        mock_http_response.status_code = 204
        mock_http_response.text = "" # No text
        
        mock_http_instance = MockHttpRequests.return_value
        mock_http_instance.http_requests.return_value = mock_http_response

        request_body = {"some": "data"}
        status, data, error = client.bitbucket_requests('post', f"{client.base_api_url}/other/endpoint", data=request_body)
        
        import json # Ensure json is imported for dumps
        MockHttpRequests.assert_called_once_with('post', f"{client.base_api_url}/other/endpoint", client.user, client.password, data=json.dumps(request_body), params=None)
        mock_http_instance.http_requests.assert_called_once()
        self.assertEqual(status, 204)
        self.assertIsNone(data)
        self.assertIsNone(error)

    @patch('atlassian_examples.bitbucket.bitbucket_client.HttpRequests')
    def test_bitbucket_requests_json_decode_error(self, MockHttpRequests):
        """Test bitbucket_requests when response is not valid JSON."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)

        mock_http_response = MagicMock()
        mock_http_response.status_code = 200
        mock_http_response.text = "Not a valid JSON"
        mock_http_response.json.side_effect = ValueError("Simulated JSONDecodeError") # Or json.JSONDecodeError
        
        mock_http_instance = MockHttpRequests.return_value
        mock_http_instance.http_requests.return_value = mock_http_response

        status, data, error = client.bitbucket_requests('get', f"{client.base_api_url}/another/endpoint")

        MockHttpRequests.assert_called_once_with('get', f"{client.base_api_url}/another/endpoint", client.user, client.password, data='null', params=None)
        self.assertEqual(status, 200)
        self.assertEqual(data, "Not a valid JSON") # Should return the raw text
        self.assertIsInstance(error, ValueError) # Check if it's a JSONDecodeError or its parent

    @patch('atlassian_examples.bitbucket.bitbucket_client.HttpRequests')
    def test_bitbucket_requests_request_exception(self, MockHttpRequests):
        """Test bitbucket_requests when HttpRequests raises a RequestException."""
        host = "http://localhost:7990"
        user = "testuser"
        password = "testpassword"
        client = BitbucketApi(host, user, password)

        # Configure the HttpRequests instance to raise an exception
        mock_http_instance = MockHttpRequests.return_value
        # Assuming HttpRequests is imported in bitbucket_client
        # from requests.exceptions import RequestException (or a more specific one if available)
        # For this test, we'll use a generic Exception as placeholder if RequestException is not directly available for import here
        # In the actual code, it would be `requests.exceptions.RequestException`
        import requests # Make sure requests is imported for the exception
        mock_http_instance.http_requests.side_effect = requests.exceptions.RequestException("Simulated network error")

        status, data, error = client.bitbucket_requests('get', f"{client.base_api_url}/error/endpoint")

        MockHttpRequests.assert_called_once_with('get', f"{client.base_api_url}/error/endpoint", client.user, client.password, data='null', params=None)
        self.assertIsNone(status)
        self.assertIsNone(data)
        self.assertIsInstance(error, requests.exceptions.RequestException)
        self.assertEqual(str(error), "Simulated network error")


if __name__ == '__main__':
    unittest.main()

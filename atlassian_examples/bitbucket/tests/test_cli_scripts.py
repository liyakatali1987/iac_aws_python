import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
import getpass # Import getpass for direct reference in patching

# Add the parent directory of 'atlassian_examples' to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # This is /tests
project_root = os.path.dirname(os.path.dirname(parent_dir)) # This is /
sys.path.insert(0, project_root)

# Import the main functions from the scripts
from atlassian_examples.bitbucket import add_default_reviewers_project
from atlassian_examples.bitbucket import add_default_reviewers_repo

class TestCliScripts(unittest.TestCase):

    @patch('atlassian_examples.bitbucket.add_default_reviewers_project.BitbucketApi')
    @patch('os.environ.get')
    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_add_default_reviewers_project_basic_input(
            self, mock_input, mock_getpass, mock_os_environ_get, MockBitbucketApi):
        """Test add_default_reviewers_project.py with basic user inputs."""
        
        # Setup mock return values for inputs
        mock_input.side_effect = [
            'http://localhost:7990', # host
            'testuser',             # user
            'TESTPROJ',             # project_key
            'user1 user2'           # user_list_input
        ]
        mock_getpass.return_value = 'testpassword'
        mock_os_environ_get.return_value = None # Ensure env vars are not used

        # Mock BitbucketApi instance and its methods
        mock_api_instance = MockBitbucketApi.return_value
        mock_api_instance.get_user_details.side_effect = [
            {'name': 'user1', 'id': 1}, 
            {'name': 'user2', 'id': 2}
        ]
        mock_api_instance.generic_add_default_reviewers_condition.return_value = (200, "Success", None)

        # Call the main function of the script
        add_default_reviewers_project.main()

        # Assertions
        mock_os_environ_get.assert_any_call('BITBUCKET_HOST')
        mock_os_environ_get.assert_any_call('BITBUCKET_USER')
        mock_os_environ_get.assert_any_call('BITBUCKET_PASSWORD')
        
        mock_input.assert_any_call('Enter host address : [e.g. http://localhost:7990] ')
        mock_input.assert_any_call('Enter userid (*required):')
        mock_getpass.assert_called_once_with(prompt='Enter password (*required): ')
        mock_input.assert_any_call('Enter project key (*required):')
        mock_input.assert_any_call('Enter space-separated user list (e.g., userA userB userC) (*required): ')

        MockBitbucketApi.assert_called_once_with('http://localhost:7990', 'testuser', 'testpassword')
        
        expected_user_calls = [call('user1'), call('user2')]
        mock_api_instance.get_user_details.assert_has_calls(expected_user_calls)
        
        expected_user_data = [{'name': 'user1', 'id': 1}, {'name': 'user2', 'id': 2}]
        expected_payload_config = {
            "sourceMatcher": {"active": True, "id": "refs/heads/**", "displayId": "refs/heads/**", "type": {"id": "PATTERN", "name": "Pattern"}},
            "targetMatcher": {"active": True, "id": "refs/heads/develop", "displayId": "develop", "type": {"id": "BRANCH", "name": "Branch"}},
            "requiredApprovals": 1
        }
        mock_api_instance.generic_add_default_reviewers_condition.assert_called_once_with(
            'TESTPROJ', expected_user_data, expected_payload_config
        )

    @patch('atlassian_examples.bitbucket.add_default_reviewers_project.BitbucketApi')
    @patch('os.environ.get')
    @patch('getpass.getpass') # Still need to patch getpass even if not called
    @patch('builtins.input')
    def test_add_default_reviewers_project_env_vars(
            self, mock_input, mock_getpass, mock_os_environ_get, MockBitbucketApi):
        """Test add_default_reviewers_project.py using environment variables for credentials."""

        # Setup mock for os.environ.get
        def environ_get_side_effect(key):
            if key == 'BITBUCKET_HOST': return 'http://envhost:7990'
            if key == 'BITBUCKET_USER': return 'envuser'
            if key == 'BITBUCKET_PASSWORD': return 'envpass'
            return None
        mock_os_environ_get.side_effect = environ_get_side_effect
        
        # Setup mock for remaining inputs
        mock_input.side_effect = [
            'TESTPROJ_ENV', # project_key
            'env_userA env_userB'      # user_list_input
        ]

        mock_api_instance = MockBitbucketApi.return_value
        mock_api_instance.get_user_details.side_effect = [
            {'name': 'env_userA', 'id': 10}, 
            {'name': 'env_userB', 'id': 20}
        ]
        mock_api_instance.generic_add_default_reviewers_condition.return_value = (201, "Created via Env", None)

        add_default_reviewers_project.main()

        # Assertions
        mock_os_environ_get.assert_any_call('BITBUCKET_HOST')
        mock_os_environ_get.assert_any_call('BITBUCKET_USER')
        mock_os_environ_get.assert_any_call('BITBUCKET_PASSWORD')

        # Assert that input and getpass were NOT called for host, user, password
        for actual_call in mock_input.call_args_list:
            args, _ = actual_call
            self.assertNotIn('Enter host address', args[0])
            self.assertNotIn('Enter userid', args[0])
        mock_getpass.assert_not_called()

        mock_input.assert_any_call('Enter project key (*required):')
        mock_input.assert_any_call('Enter space-separated user list (e.g., userA userB userC) (*required): ')

        MockBitbucketApi.assert_called_once_with('http://envhost:7990', 'envuser', 'envpass')
        
        expected_user_data = [{'name': 'env_userA', 'id': 10}, {'name': 'env_userB', 'id': 20}]
        mock_api_instance.generic_add_default_reviewers_condition.assert_called_once_with(
            'TESTPROJ_ENV', expected_user_data, unittest.mock.ANY # payload_config is standard
        )

    @patch('atlassian_examples.bitbucket.add_default_reviewers_repo.BitbucketApi')
    @patch('os.environ.get')
    @patch('getpass.getpass')
    @patch('builtins.input')
    def test_add_default_reviewers_repo_basic_input(
            self, mock_input, mock_getpass, mock_os_environ_get, MockBitbucketApi):
        """Test add_default_reviewers_repo.py with basic user inputs."""
        
        # Setup mock return values for inputs
        mock_input.side_effect = [
            'http://localhost:7990', # host
            'testuser_repo',         # user
            'TESTPROJ_R',           # project_key
            'test-repo-name',       # repo_name
            'userA_repo userB_repo' # user_list_input
        ]
        mock_getpass.return_value = 'testpassword_repo'
        mock_os_environ_get.return_value = None # Ensure env vars are not used

        mock_api_instance = MockBitbucketApi.return_value
        mock_api_instance.get_user_details.side_effect = [
            {'name': 'userA_repo', 'id': 101}, 
            {'name': 'userB_repo', 'id': 102}
        ]
        mock_api_instance.generic_add_default_reviewers_condition.return_value = (200, "Repo Success", None)

        add_default_reviewers_repo.main()

        mock_os_environ_get.assert_any_call('BITBUCKET_HOST')
        mock_os_environ_get.assert_any_call('BITBUCKET_USER')
        mock_os_environ_get.assert_any_call('BITBUCKET_PASSWORD')
        
        mock_input.assert_any_call('Enter host address : [e.g. http://localhost:7990] ')
        mock_input.assert_any_call('Enter userid (*required):')
        mock_getpass.assert_called_once_with(prompt='Enter password (*required): ')
        mock_input.assert_any_call('Enter Project Key (*required): ')
        mock_input.assert_any_call('Enter repository name (*required):')
        mock_input.assert_any_call('Enter space-separated user list (e.g., userA userB userC) (*required): ')

        MockBitbucketApi.assert_called_once_with('http://localhost:7990', 'testuser_repo', 'testpassword_repo')
        
        expected_user_calls = [call('userA_repo'), call('userB_repo')]
        mock_api_instance.get_user_details.assert_has_calls(expected_user_calls)
        
        expected_user_data = [{'name': 'userA_repo', 'id': 101}, {'name': 'userB_repo', 'id': 102}]
        expected_payload_config = { # This is the standard payload config
            "sourceMatcher": {"active": True, "id": "refs/heads/**", "displayId": "refs/heads/**", "type": {"id": "PATTERN", "name": "Pattern"}},
            "targetMatcher": {"active": True, "id": "refs/heads/develop", "displayId": "develop", "type": {"id": "BRANCH", "name": "Branch"}},
            "requiredApprovals": 1
        }
        mock_api_instance.generic_add_default_reviewers_condition.assert_called_once_with(
            'TESTPROJ_R', expected_user_data, expected_payload_config, repo_name='test-repo-name'
        )

    @patch('atlassian_examples.bitbucket.add_default_reviewers_repo.BitbucketApi')
    @patch('os.environ.get')
    @patch('getpass.getpass') 
    @patch('builtins.input')
    def test_add_default_reviewers_repo_env_vars(
            self, mock_input, mock_getpass, mock_os_environ_get, MockBitbucketApi):
        """Test add_default_reviewers_repo.py using environment variables for credentials."""

        def environ_get_side_effect(key):
            if key == 'BITBUCKET_HOST': return 'http://envhost_repo:7990'
            if key == 'BITBUCKET_USER': return 'envuser_repo'
            if key == 'BITBUCKET_PASSWORD': return 'envpass_repo'
            return None
        mock_os_environ_get.side_effect = environ_get_side_effect
        
        mock_input.side_effect = [
            'TESTPROJ_R_ENV',         # project_key
            'test-repo-name-env',     # repo_name
            'env_userA_r env_userB_r' # user_list_input
        ]

        mock_api_instance = MockBitbucketApi.return_value
        mock_api_instance.get_user_details.side_effect = [
            {'name': 'env_userA_r', 'id': 110}, 
            {'name': 'env_userB_r', 'id': 120}
        ]
        mock_api_instance.generic_add_default_reviewers_condition.return_value = (201, "Created Repo via Env", None)

        add_default_reviewers_repo.main()

        mock_os_environ_get.assert_any_call('BITBUCKET_HOST')
        mock_os_environ_get.assert_any_call('BITBUCKET_USER')
        mock_os_environ_get.assert_any_call('BITBUCKET_PASSWORD')

        for actual_call in mock_input.call_args_list:
            args, _ = actual_call
            self.assertNotIn('Enter host address', args[0])
            self.assertNotIn('Enter userid', args[0])
        mock_getpass.assert_not_called()

        mock_input.assert_any_call('Enter Project Key (*required): ')
        mock_input.assert_any_call('Enter repository name (*required):')
        mock_input.assert_any_call('Enter space-separated user list (e.g., userA userB userC) (*required): ')

        MockBitbucketApi.assert_called_once_with('http://envhost_repo:7990', 'envuser_repo', 'envpass_repo')
        
        expected_user_data = [{'name': 'env_userA_r', 'id': 110}, {'name': 'env_userB_r', 'id': 120}]
        mock_api_instance.generic_add_default_reviewers_condition.assert_called_once_with(
            'TESTPROJ_R_ENV', expected_user_data, unittest.mock.ANY, repo_name='test-repo-name-env'
        )

if __name__ == '__main__':
    unittest.main()

import json
import requests # Import requests for exception handling
from http_req import HttpRequests

# returns the bitbucket client


class BitbucketApi:
    def __init__(self, host, user, password):
        """Initializing the class variables."""
        self.base_api_url = f'{host}/rest/api/latest'
        self.base_default_reviewers_url = f'{host}/rest/default-reviewers/latest'
        self.user = user
        self.password = password

    def get_user_details(self, user_id):
        url = f"{self.base_api_url}/admin/users?filter={user_id}"
        _, response, error = self.bitbucket_requests('get', url) # status is unused
        if error:
            # Handle error appropriately, perhaps log it or raise an exception
            print(f"Error fetching user details: {error}")
            return None
        if response and 'values' in response:
            for user in response['values']:
                if user['name'] == user_id:
                    return user
        return None

    def generic_add_default_reviewers_condition(self, project_key, users_details_list, reviewers_payload_config, repo_name=None):
        """
        Adds a default reviewer condition at the project or repository level.
        """
        if repo_name:
            url = f"{self.base_default_reviewers_url}/projects/{project_key}/repos/{repo_name}/condition"
        else:
            url = f"{self.base_default_reviewers_url}/projects/{project_key}/condition"

        data = {
            "reviewers": users_details_list,
            "sourceMatcher": reviewers_payload_config["sourceMatcher"],
            "targetMatcher": reviewers_payload_config["targetMatcher"],
            "requiredApprovals": reviewers_payload_config["requiredApprovals"]
        }
        return self.bitbucket_requests('post', url, data=data)

    def bitbucket_requests(self, req_type, url, data=None, params=None):
        try:
            response = HttpRequests(req_type, url, self.user,
                                    self.password, data=json.dumps(data), params=params).http_requests()
            if response.text:
                try:
                    return response.status_code, response.json(), None
                except json.JSONDecodeError as e:
                    return response.status_code, response.text, e
            else:
                return response.status_code, None, None
        except requests.exceptions.RequestException as e:
            return None, None, e

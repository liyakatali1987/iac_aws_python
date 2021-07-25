import json
from http_req import HttpRequests
from getpass import getpass

# This script will help user to create a bitbucket project.


def validate_inputs(values):
    if None in values:
        raise Exception('Invalid Value Provided')


class BitbucketApi:
    def __init__(self, host, user, password):
        """Initializing Class Variables."""
        self.host = f'{host}/rest/api/latest'
        self.user = user
        self.password = password

    def __bitbucket_requests(self, type, url, data=None):
        try:
            response = HttpRequests(type, url, self.user,
                                    self.password, data=json.dumps(data)).http_requests()
            if response.text:
                return response.status_code, response.json()
            else:
                return response.status_code, None
        except Exception as e:
            return None, e

    def create_project(self):
        project_key = input('Enter project key (*required): ')
        validate_inputs([project_key])
        description = input('Enter Description (optional) : ')
        url = f'{self.host}/projects'
        data = {'name': project_key, 'key': project_key,
                'description': description if description else f'New Project {project_key}'}

        return self.__bitbucket_requests('post', url, data)


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid : ')
password = getpass(prompt='Enter password : ')

try:
    validate_inputs([host, user, password])
    bb_api = BitbucketApi(host, user, password)
    status, response = bb_api.create_project()
    print(status, response)
except Exception as e:
    print(e)

from bitbucket_client import BitbucketApi
from getpass import getpass


"""
    The demostration shows how to get a user's details

"""


def get_user_details(bb_client, user_id):
    url = f"{bb_client.host}/admin/users?filter={user_id}"
    status, response = bb_client.bitbucket_requests('get', url)
    for user in response['values']:
        if user['name'] == user_id:
            return user


def add_default_reviewers(bb_client, project_key, repo_name, users):
    data = {
        "reviewers": [
            {
                "name": "test-1",
                "emailAddress": "jane@example.com",
                "id": 101,
                "displayName": "Jane Citizen",
                "active": True,
                "slug": "jcitizen",
                "type": "NORMAL"
            }
        ],
        "sourceMatcher": {
            "active": True,
            "id": "refs/heads/**",
            "displayId": "refs/heads/**",
            "type": {
                "id": "PATTERN",
                "name": "Pattern"
            }
        },
        "targetMatcher": {
            "active": True,
            "id": "refs/heads/develop",
            "displayId": "develop",
            "type": {
                "id": "BRANCH",
                "name": "Branch"
            }
        },
        "requiredApprovals": 1
    }
    user_data = []
    for user in users:
        user_details = get_user_details(bb_client, user)
        user_data.append(user_details)

    data['reviewers'] = user_data
    url = f"{bb_client.host.replace('api','default-reviewers')}/projects/{project_key}/repos/{repo_name}/condition"
    status, response = bb_client.bitbucket_requests('post', url, data=data)
    return status, response


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid (*required):')
password = getpass(prompt='Enter password (*required): ')
project_key = input('Enter Project Key (*required): ')
repo_name = input('Enter repository name (*required):')
user_list = input(
    'Enter user list (*required): ').split() or ['10001', '10002', '10003']
bb_clinet = BitbucketApi(host, user, password)

status, response = add_default_reviewers(
    bb_clinet, project_key, repo_name, user_list)
print(status, response)

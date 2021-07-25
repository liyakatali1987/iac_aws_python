from bitbucket_client import BitbucketApi
from getpass import getpass

# The demostration shows how to add multiple users to a bitbucker group


def get_user_details(bb_client, user_id):
    url = f"{bb_client.host}/admin/users?filter={user_id}"
    status, response = bb_client.bitbucket_requests('get', url)
    print(status)
    for user in response['values']:
        if user['name'] == user_id:
            return user


def create_reviewers_group(bb_client, project_key, group_name, user_list):
    user_data = []
    for user in user_list:
        user_details = get_user_details(bb_client, user)
        user_data.append(user_details)

    url = f"{bb_client.host}/projects/{project_key}/settings/reviewer-groups"
    data = {'name': group_name, 'description': 'test', 'users': user_data}
    status, response = bb_client.bitbucket_requests('post', url, data=data)
    return status, response


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid (*required):')
password = getpass(prompt='Enter password (*required): ')
project_key = input('Enter project key (*required): ')
group_name = input('Enter group name (*required): ')
# user list input should be in format user1 user2 user3
user_list = input('Enter users list (*required): ').split()

bb_clinet = BitbucketApi(host, user, password)

status, response = create_reviewers_group(
    bb_clinet, project_key, group_name, user_list)
print(status, response)

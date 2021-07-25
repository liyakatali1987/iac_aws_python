from bitbucket_client import BitbucketApi
from getpass import getpass

# The demostration shows how to add users to a group


def add_users_to_group(bb_client, group_name, user_list):
    url = f"{bb_client.host}/admin/groups/add-users"
    data = {"group": group_name, "users": user_list}
    status, response = bb_client.bitbucket_requests('post', url, data=data)
    return status, response


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid (*required):')
password = getpass(prompt='Enter password (*required): ')

group_name = input('Enter group name (*required): ')
# user list input should be in format user1 user2 user3
user_list = input('Enter users list (*required): ').split()

bb_clinet = BitbucketApi(host, user, password)
status, user_details = add_users_to_group(bb_clinet, group_name, user_list)
print(status, user_details)

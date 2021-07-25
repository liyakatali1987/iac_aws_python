
from getpass import getpass
from bitbucket_client import BitbucketApi

# The demostration shows how to add users in bitbucket.
# Not adding input validation and leaving this to the user to implement a validation logic.


def create_bitbuck_groups(bb_client, group_name):
    url = f'{bb_client.host}/admin/groups'
    params = {'name': group_name}
    data = {'name': group_name, 'deletable': True}
    status, response = bb_client.bitbucket_requests(
        'post', url, data=data, params=params)
    return status, response


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid (*required):')
password = getpass(prompt='Enter password (*required): ')
group_name = input('Enter group name (*required): ')

bb_client = BitbucketApi(host, user, password)
status, response = create_bitbuck_groups(bb_client, group_name)
print(status, response)

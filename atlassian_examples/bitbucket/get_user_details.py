from bitbucket_client import BitbucketApi
from getpass import getpass


""" The demostration shows how to get a user's details"""


def get_user_details(bb_client, user_id):
    url = f"{bb_client.host}/admin/users?filter={user_id}"
    status, response = bb_client.bitbucket_requests('get', url)
    for user in response['values']:
        if user['name'] == user_id:
            return user


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid (*required):')
password = getpass(prompt='Enter password (*required): ')

bb_clinet = BitbucketApi(host, user, password)
user_details = get_user_details(bb_clinet, 'bitbucket_user-1')
print(user_details)

from bitbucket_client import BitbucketApi
from getpass import getpass


""" The demostration shows how to list all the users in bitbucket server
"""


def list__bitbucket_users(bb_client):
    url = f'{bb_client.host}/admin/users'
    user_data = []
    status, response = bb_client.bitbucket_requests('get', url)
    user_data.extend(response['values'])

    while not response['isLastPage']:
        url = f"{bb_client.host}/admin/users?start={response['nextPageStart']}"
        print(url)
        status, response = bb_client.bitbucket_requests('get', url)
        user_data.extend(response['values'])

    return user_data


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid (*required):')
password = getpass(prompt='Enter password (*required): ')

bb_client = BitbucketApi(host, user, password)

response = list__bitbucket_users(bb_client)
print(response)

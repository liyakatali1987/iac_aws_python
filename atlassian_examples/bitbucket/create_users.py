from bitbucket_client import BitbucketApi
from getpass import getpass


# The demostration shows how to add users in bitbucket.
# Set notify to true the create user will be notified via email their account has been created
# and requires a password to be reset.
# This option can only be used if a mail server has been configured


def create_bitbuck_user(bb_client, user_name, password, display_name, email, add_to_default_group=False, notify=False):
    url = f'{bb_client.host}/admin/users'
    params = {'name': user_name, 'password': password,
              'displayName': display_name, 'emailAddress': email, 'addToDefaultGroup': add_to_default_group, 'notify': notify}
    status, response = bb_client.bitbucket_requests('post', url, params=params)
    return status, response


host = input(
    'Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'
user = input('Enter userid (*required):')
password = getpass(prompt='Enter password (*required): ')

# Enter user details need to be created

print('Enter user details need to be created')

user_name = input('Enter username  (*required):')
user_password = getpass(
    prompt='Enter users password (*required)') or f'{user_name}000'
display_name = input('Enter display name (*required):') or user_name
email = input(
    'Enter email address (*required):') or f'{user_name}@testmail.com'

bb_client = BitbucketApi(host, user, password)

status, response = create_bitbuck_user(
    bb_client, user_name, user_password, display_name, email)
print(status, response)

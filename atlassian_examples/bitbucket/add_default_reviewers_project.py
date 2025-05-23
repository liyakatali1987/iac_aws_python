import os # Import os module
from bitbucket_client import BitbucketApi
from getpass import getpass

# The demostration shows add default reviewers into a project.

def main():
    # Read host from environment variable or prompt
    host = os.environ.get('BITBUCKET_HOST')
    if not host:
        host = input('Enter host address : [e.g. http://localhost:7990] ') or 'http://localhost:7990'

    # Read user from environment variable or prompt
    user = os.environ.get('BITBUCKET_USER')
    if not user:
        user = input('Enter userid (*required):')

    # Read password from environment variable or prompt
    password = os.environ.get('BITBUCKET_PASSWORD')
    if not password:
        password = getpass(prompt='Enter password (*required): ')

    project_key = input('Enter project key (*required):')

    # Standardize user_list handling
    user_input_str = input('Enter space-separated user list (e.g., userA userB userC) (*required): ')
    if not user_input_str:
        user_list = ['10001', '10002', '10003'] # Default if empty input
    else:
        user_list = user_input_str.split()


    bb_client = BitbucketApi(host, user, password)

    user_data = []
    for user_id_from_list in user_list:
        user_details = bb_client.get_user_details(user_id_from_list)
        if user_details:
            user_data.append(user_details)
        else:
            print(f"Warning: Could not retrieve details for user {user_id_from_list}")

    if not user_data:
        print("No valid user details found. Aborting.")
    else:
        payload_config = {
            "sourceMatcher": {
                "active": True,
                "id": "refs/heads/**",
                "displayId": "refs/heads/**",
                "type": {"id": "PATTERN", "name": "Pattern"}
            },
            "targetMatcher": {
                "active": True,
                "id": "refs/heads/develop",
                "displayId": "develop",
                "type": {"id": "BRANCH", "name": "Branch"}
            },
            "requiredApprovals": 1
        }

        status, response, error = bb_client.generic_add_default_reviewers_condition(project_key, user_data, payload_config)
        if error:
            print(f"Error adding default reviewers: {error}")
            print(status, response)
        else:
            print(status, response)

if __name__ == '__main__':
    main()

import os
from boto3 import Session # Still needed for Session().available_profiles in get_aws_profile
from aws_scripts.common_aws_client import AWS # Import the AWS class


def get_aws_profile_interactive():
    """Interactively prompts user to select an AWS profile from available 'ams' profiles."""
    try:
        profiles = Session().available_profiles
    except Exception as e:
        print(f"Error listing available AWS profiles: {e}. Using 'default'.")
        return 'default'

    ams_profiles = [p for p in profiles if 'ams' in p]
    if not ams_profiles:
        print("No 'ams' profiles found. Using 'default'.")
        return 'default'
    ams_profiles.sort()
    print("Available 'ams' profiles:")
    for i, profile_name in enumerate(ams_profiles):
        print(f'Press {i+1} For -> {profile_name}')

    try:
        choice = input('Enter Your Choice: ')
        return ams_profiles[int(choice)-1]
    except (ValueError, IndexError, EOFError): # Handle invalid input or EOF
        print('Invalid choice or input error. Setting ams01-nonprod as default value (if available, else default).')
        return 'ams01-nonprod' if 'ams01-nonprod' in ams_profiles else 'default'


def delete_stacks_logic(aws_client, stacks_filter):
    """Handles the logic of listing and deleting CloudFormation stacks."""
    client = aws_client.get_client('cloudformation')
    if not client:
        print("Failed to get CloudFormation client. Exiting.")
        return

    paginator = client.get_paginator('describe_stacks')
    response_iterator = paginator.paginate()
    stack_list = []

    print("Listing stacks matching filter:", stacks_filter)
    if not stacks_filter:
        print('stacks_filter value is required.')
        return # Changed exit(1) to return for better testability

    for page in response_iterator:
        for stack_details in page['Stacks']:
            if stacks_filter in stack_details['StackName']:
                stack_list.append(stack_details['StackName'])

    print("\nStacks to be deleted:")
    if not stack_list:
        print("No stacks found matching the filter.")
        return
    for s_name in stack_list:
        print(s_name)
    user_input = input('Press y to continue with deletion of the above stacks: ')

    if user_input.lower() == 'y':
        print('\nDeleting Stacks...')
        waiter = client.get_waiter('stack_delete_complete')
        # Consider writing to a more robust location or handling file errors
        try:
            with open('stack_list_deleted.csv', 'w') as f:
                for stack_name_to_delete in stack_list:
                    print(f'Deleting stack: {stack_name_to_delete}')
                    try:
                        client.delete_stack(StackName=stack_name_to_delete)
                        waiter.wait(StackName=stack_name_to_delete, WaiterConfig={
                            'Delay': 30,
                            'MaxAttempts': 50
                        })
                        f.write(stack_name_to_delete + "\n")
                        print(f"Successfully deleted stack: {stack_name_to_delete}")
                    except Exception as e:
                        print(f"Error deleting stack {stack_name_to_delete}: {e}")
                        # Decide if you want to continue with other stacks or stop
        except IOError as e:
            print(f"Error opening or writing to file stack_list_deleted.csv: {e}")
    else:
        print("Deletion aborted by user.")

def main():
    region_name = os.environ.get('AWS_REGION') or 'ap-southeast-2'
    # Get AWS profile: from env var first, then interactive, then default
    aws_profile_env = os.environ.get('AWS_PROFILE')
    if aws_profile_env:
        aws_profile = aws_profile_env
        print(f"Using AWS Profile from environment variable: {aws_profile}")
    else:
        aws_profile = get_aws_profile_interactive()
        print(f'Selected AWS Profile: {aws_profile}')

    stacks_filter_input = input('Enter Stack filter (e.g., part of stack name): ').strip()
    if not stacks_filter_input:
        print("Stack filter cannot be empty.")
        return

    try:
        aws_connection = AWS(region_name=region_name, aws_profile=aws_profile)
        delete_stacks_logic(aws_connection, stacks_filter_input)
    except Exception as e:
        # Catching exceptions from AWS connection or client creation
        print(f"An error occurred during AWS setup or stack deletion process: {e}")

if __name__ == '__main__':
    main()

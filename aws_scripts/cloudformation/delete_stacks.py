from boto3 import Session
from botocore.config import Config

config = Config(
    retries=dict(
        max_attempts=15
    ),
    region_name='ap-southeast-2'
)


def get_aws_profile():

    profiles = Session().available_profiles

    ams_profiles = []

    for profile in profiles:
        if 'ams' in profile:
            ams_profiles.append(profile)
    ams_profiles.sort()
    for i, profile in enumerate(ams_profiles):
        print(f'Press {i+1} For -> {profile}')

    profile = input('Enter Your Choice: ')

    try:
        return ams_profiles[int(profile)-1]
    except Exception:
        print('Invalid Profile Selected, Setting ams01-nonprod as default value')
        return 'ams01-nonprod'


def delete_stacks(filter, profile_name='default'):

    session = Session(profile_name=profile_name)

    client = session.client('cloudformation', config=config)
    paginator = client.get_paginator('describe_stacks')
    response_iterator = paginator.paginate()
    stack_list = []

    print("Listing stacks:")
    if not filter:
        print('Filter values is required')
        exit(1)

    for stacks in response_iterator:
        stacks = stacks['Stacks']
        for stack in stacks:
            if filter in stack['StackName']:
                stack_list.append(stack['StackName'])

    print("Stacks to be deleted")
    print(stack_list)
    if stack_list:
        user_input = input('Press y to continue: ')

        if user_input == 'y':
            print('Deleting Stacks')
            waiter = client.get_waiter('stack_delete_complete')
            with open('stack_list.csv', 'w') as f:
                for stack in stack_list:
                    print('Deleting stack: {}'.format(stack))
                    try:
                        client.delete_stack(StackName=stack)
                        waiter.wait(StackName=stack, WaiterConfig={
                            'Delay': 30,
                            'MaxAttempts': 50
                        })
                    except Exception as e:
                        raise e
                    f.write(stack+"\n")

                f.close()


aws_profile = get_aws_profile()
print(f'Selected AWS Profile: {aws_profile}')
filter = input('Enter Stack Filter: ').strip()


delete_stacks(filter, aws_profile)

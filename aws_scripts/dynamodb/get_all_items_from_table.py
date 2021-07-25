from aws_conn import AWS


def get_all_items(table_name,
                  attributes_to_get=None,
                  region_name=None,
                  aws_profile='default'):

    aws_obj = AWS(region_name=region_name, aws_profile=aws_profile)
    client = aws_obj.get_client('dynamodb')
    paginator = client.get_paginator('scan')

    if attributes_to_get:
        args = {'TableName': table_name, 'AttributesToGet': attributes_to_get}
    else:
        args = {'TableName': table_name}

    response_iterator = paginator.paginate(**args)

    data = []
    for response in response_iterator:
        for items in response['Items']:
            data.append(items)

    return data


table_name = input('Enter table_name : ').strip()
attributes_to_get = input(
    'Enter attributes to get (optional) add space between values : ')
region_name = input('Enter AWS region_name : ').strip()

aws_profile = input('Enter AWS profile (optional) : ')

attributes_to_get = attributes_to_get.split()

data = get_all_items(table_name, attributes_to_get=attributes_to_get,
                     region_name=region_name, aws_profile=aws_profile)


print(data)

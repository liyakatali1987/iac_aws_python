from aws_conn import AWS


# NOTE: key and value are the fileds in the table.
# You need to modify the code according to your table structure


def add_item(table_name,
             key, value,
             region_name='ap-southeast-2',
             aws_profile='default'):
    aws_obj = AWS(region_name=region_name, aws_profile=aws_profile)
    resource = aws_obj.get_resource('dynamodb')
    table = resource.Table(table_name)
    args = {
        'Item': {'key': key, 'value': value},
    }

    response = table.put_item(**args)
    return response

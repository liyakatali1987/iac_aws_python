from aws_conn import AWS

"""
    NOTE: Supply attributes_to_get as a list e.g. ['attr1', 'attr2']
"""


def get_item(table_name, key, value, region_name='ap-southeast-2', aws_profile='default', attributes_to_get=None):
    aws_obj = AWS(region_name=region_name, aws_profile=aws_profile)
    resource = aws_obj.get_resource('dynamodb')
    table = resource.Table(table_name)
    args = None
    if attributes_to_get:
        args = {'Key': {key: value},
                'AttributesToGet': attributes_to_get}
    else:
        args = {'Key': {key: value}}

    response = table.get_item(**args)
    return response['Item']

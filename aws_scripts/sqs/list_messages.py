from aws_scripts.common_aws_client import AWS


def list_sqs_messages(queue_url,
                      region_name='ap-southeast-2',
                      aws_profile='default'):

    aws_obj = AWS(region_name=region_name, aws_profile=aws_profile)
    sqs = aws_obj.get_resource('sqs')
    queue = sqs.Queue(queue_url)
    messages = queue.receive_messages()
    return messages

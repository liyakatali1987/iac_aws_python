from boto3 import Session
from botocore.config import Config
from datetime import datetime
from dateutil import parser


config = Config(
    retries=dict(
        max_attempts=15
    ),
    region_name="ap-southeast-2")


# Update the profile name according to your configuration
# replace the default with the prifle profile name if using different aws profile
session = Session(profile_name='default')

current_month = datetime.now().month

client = session.client('ec2', config=config)
response = client.describe_images(Owners=['amazon'],
                                  Filters=[
                                      {
                                          'Name': 'platform',
                                          'Values': ['windows']
                                      },
                                      {
                                          'Name': 'is-public',
                                          'Values': ['true']
                                      },
                                      {
                                          'Name': 'name',
                                          'Values': [
                                              'Windows_Server-2012-R2_RTM-English-64Bit-Base*',
                                              'Windows_Server-2016-English-Full-Base*',
                                              'Windows_Server-2019-English-Full-Base*']
                                      }
])


images = response['Images']
for image in images:
    create_date = parser.parse(image['CreationDate'])
    if create_date.month == current_month:
        print(f'{image["Name"]}, {image["ImageId"]}, {create_date}')

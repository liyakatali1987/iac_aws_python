import os
from datetime import datetime
from dateutil import parser
from aws_scripts.common_aws_client import AWS # Import the AWS class


def get_latest_amis():
    # Obtain region_name and aws_profile from environment variables or use defaults
    region_name = os.environ.get('AWS_REGION') or "ap-southeast-2"
    aws_profile = os.environ.get('AWS_PROFILE') or "default"

    # Instantiate the AWS client
    aws_connection = AWS(region_name=region_name, aws_profile=aws_profile)
    
    # Get the EC2 client
    client = aws_connection.get_client('ec2')
    
    if not client:
        print("Failed to get EC2 client. Exiting.") # Or handle error more robustly
        return

    current_month = datetime.now().month
    
    try:
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
                print(f'{image["Name"]}, {image["ImageId"]}, {image["CreationDate"]}')
    except Exception as e:
        print(f"Error describing images: {e}")

if __name__ == '__main__':
    get_latest_amis()

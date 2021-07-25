from boto3 import Session
from botocore.config import Config


class AWS:
    def __init__(self, region_name, aws_profile):
        """Required parameters for AWS connection."""
        self.config = Config(
            region_name=region_name,
            retries={
                'max_attempts': 30,
                'mode': 'standard'
            }
        )

        self.session = Session(profile_name=aws_profile)

    def get_client(self, service):
        try:
            return self.session.client(service, config=self.config)
        except Exception as e:
            return e

    def get_resource(self, service):
        try:
            return self.session.resource(service, config=self.config)
        except Exception as e:
            return e

from boto3 import Session
from botocore.config import Config
import logging # Using logging for errors

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        self.aws_profile = aws_profile # Store profile name if needed for session creation
        try:
            self.session = Session(profile_name=aws_profile, region_name=region_name)
        except Exception as e:
            logging.error(f"Error creating AWS session (profile: {aws_profile}, region: {region_name}): {e}")
            raise

    def get_client(self, service):
        try:
            return self.session.client(service, config=self.config)
        except Exception as e:
            logging.error(f"Error getting AWS client for service '{service}' (profile: {self.aws_profile}, region: {self.config.region_name}): {e}")
            raise 

    def get_resource(self, service):
        try:
            return self.session.resource(service, config=self.config)
        except Exception as e:
            logging.error(f"Error getting AWS resource for service '{service}' (profile: {self.aws_profile}, region: {self.config.region_name}): {e}")
            raise

import os
from aws_scripts.common_aws_client import AWS # Import the AWS class

def delete_ebs_snap_logic(ec2_client, snap_id):
    """Deletes a specific EBS snapshot."""
    print(f"Attempting to delete snapshot {snap_id}...")
    try:
        response = ec2_client.delete_snapshot(SnapshotId=snap_id)
        print("Successfully initiated deletion of snapshot.")
        print("Response:", response)
        return True
    except Exception as e:
        print(f"Error deleting snapshot {snap_id}: {e}")
        return False

def main():
    region_name = os.environ.get('AWS_REGION') or "ap-southeast-2"
    aws_profile = os.environ.get('AWS_PROFILE') or "default"

    aws_connection = AWS(region_name=region_name, aws_profile=aws_profile)
    ec2_client_instance = aws_connection.get_client('ec2')

    if not ec2_client_instance:
        print("Failed to get EC2 client. Exiting.")
        return

    snapshot_id_to_delete = input("Enter the Snapshot ID to delete: ").strip()
    if not snapshot_id_to_delete:
        print("Snapshot ID cannot be empty.")
        return

    delete_ebs_snap_logic(ec2_client_instance, snapshot_id_to_delete)

if __name__ == '__main__':
    main()

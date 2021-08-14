import boto3

ec2_client = boto3.client('ec2', region_name='ap-southeast-2')


def delete_ebs_snaps(snap_id):
    print("deleting snapshot {}".format(snap_id))
    try:
        response = ec2_client.delete_snapshot(
            SnapshotId=snap_id,
        )
        print(response)

    except Exception as e:
        print(e)


delete_ebs_snaps('snapshot_id')

# Python Automation Scripts for IT Operations

This repository contains a collection of Python scripts designed to automate
various tasks related to IT operations, including interactions with Atlassian
Bitbucket, Amazon Web Services (AWS), and Active Directory.

## Prerequisites

*   Python 3.x
*   Install required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Most scripts in this repository are configured primarily through **environment
variables**. This approach enhances security (especially for credentials) and is
convenient for automated execution in CI/CD pipelines or scheduled tasks.
If the required environment variables are not set, many scripts will fall back to
**interactive prompts** to gather the necessary information.

### Key Environment Variables:

*   **Atlassian Bitbucket Scripts:**
    *   `BITBUCKET_HOST`: The base URL of your Bitbucket instance (e.g.,
        `http://localhost:7990` or `https://bitbucket.yourcompany.com`).
    *   `BITBUCKET_USER`: Your Bitbucket username.
    *   `BITBUCKET_PASSWORD`: Your Bitbucket password or personal access token.

*   **AWS Scripts:**
    *   `AWS_REGION`: The AWS region to target (e.g., `ap-southeast-2`,
        `us-east-1`). Defaults to `ap-southeast-2` in many scripts if not set.
    *   `AWS_PROFILE`: The AWS CLI profile name to use for credentials and
        configuration. Defaults to `default` in many scripts if not set.
    *   *Note: Some individual AWS scripts might accept or require additional
        parameters via command-line arguments or specific environment
        variables.*

*   **Active Directory Scripts:**
    *   `AD_SERVER`: The hostname or IP address of your Active Directory domain
        controller (e.g., `ad.example.com`).
    *   `AD_PORT`: The port number for LDAP/LDAPS communication (e.g., `389` for
        LDAP, `636` for LDAPS). Defaults to `636` (LDAPS) if not set.
    *   `AD_USER`: Your Active Directory username (e.g., `DOMAIN\username` or
        `username@domain.com`).
    *   `AD_PASS`: Your Active Directory password.

## Script Categories

### 1. Atlassian Bitbucket Scripts:

*   **Purpose:** Scripts for interacting with Bitbucket Server/Data Center APIs.
    Current functionalities include managing default reviewers for projects and
    repositories.
*   **Location:** `atlassian_examples/bitbucket/`
*   **Details:** These scripts utilize a common HTTP request handler and a
    Bitbucket API client class for interacting with the Bitbucket REST APIs.

### 2. AWS Scripts:

*   **Purpose:** A collection of scripts designed to automate various tasks
    within Amazon Web Services. This includes managing EC2 AMIs, interacting
    with DynamoDB tables, listing SQS messages, deleting CloudFormation stacks,
    and managing EBS snapshots.
*   **Common Client:** Most AWS scripts leverage a shared AWS client wrapper
    located in `aws_scripts/common_aws_client.py`, which standardizes session
    creation and client/resource retrieval from `boto3`.
*   **Location:** `aws_scripts/`
    *   `aws_scripts/cloudformation/`: Scripts for CloudFormation stack
        operations.
    *   `aws_scripts/dynamodb/`: Scripts for DynamoDB table interactions.
    *   `aws_scripts/ebs/`: Scripts for EBS volume and snapshot management.
    *   `aws_scripts/ec2/`: Scripts for EC2 instance and AMI management.
    *   `aws_scripts/sqs/`: Scripts for SQS queue operations.

### 3. Active Directory Scripts:

*   **Purpose:** Scripts for performing operations against Active Directory,
    such as searching for users and retrieving their attributes.
*   **Location:** `activedir/`
*   **Details:** The `active_dir_ops.py` script uses the `ldap3` library to
    connect and interact with Active Directory over LDAP or LDAPS.

## Usage

Navigate to the specific script's directory and execute it using Python.
Ensure you have configured the necessary environment variables or be prepared
to enter details interactively when prompted.

For example, to run an AWS script:

```bash
# Set environment variables (example for Linux/macOS)
export AWS_PROFILE="your-aws-profile"
export AWS_REGION="your-aws-region"

# Navigate and run
cd aws_scripts/ec2/
python get_latest_windows_amis.py
```

Refer to individual script files for more specific instructions or parameters
they might accept.

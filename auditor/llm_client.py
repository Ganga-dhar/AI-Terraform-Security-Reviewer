import os

import boto3


def create_client():

    region = os.getenv(
        "AWS_REGION",
        "us-east-1"
    )

    return boto3.client(
        "bedrock-runtime",
        region_name=region,
    )
    
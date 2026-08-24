# import os

# import boto3


# def create_client():

#     region = os.getenv(
#         "AWS_REGION",
#         "us-east-1"
#     )

#     return boto3.client(
#         "bedrock-runtime",
#         region_name=region,
#     )

import boto3
from langchain_aws import ChatBedrockConverse


def create_client():

    return ChatBedrockConverse(
        model="us.amazon.nova-lite-v1:0",
        region_name="us-east-1",
        temperature=0,
    )
   
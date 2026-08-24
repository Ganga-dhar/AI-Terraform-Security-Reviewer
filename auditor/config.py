import os


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "amazon.nova-lite-v1:0"
)

MAX_TOKENS = int(
    os.getenv("BEDROCK_MAX_TOKENS", "2000")
)

TEMPERATURE = float(
    os.getenv("BEDROCK_TEMPERATURE", "0")
)



#export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
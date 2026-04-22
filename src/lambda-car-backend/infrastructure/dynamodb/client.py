import boto3
from infrastructure.dynamodb.config import load_dynamodb_config


def create_dynamodb_resource():
    config = load_dynamodb_config()

    kwargs = {
        "service_name": "dynamodb",
        "region_name": config.region_name,
    }

    if config.endpoint_url:
        kwargs["endpoint_url"] = config.endpoint_url

    return boto3.resource(**kwargs)
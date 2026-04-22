import boto3
from infrastructure.dynamodb.config import load_dynamodb_config


def create_dynamodb_resource():
    config = load_dynamodb_config()
    return boto3.resource("dynamodb", region_name=config.region_name)
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class DynamoDbConfig:
    region_name: str
    endpoint_url: str | None
    users_table: str
    trips_table: str
    cars_table: str
    refuelings_table: str
    commits_table: str


def load_dynamodb_config() -> DynamoDbConfig:
    return DynamoDbConfig(
        region_name=os.getenv("AWS_REGION", "eu-west-1"),
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT_URL"),
        users_table=os.getenv("USERS_TABLE_NAME", "users"),
        trips_table=os.getenv("TRIPS_TABLE_NAME", "trips"),
        cars_table=os.getenv("CARS_TABLE_NAME", "cars"),
        refuelings_table=os.getenv("REFUELINGS_TABLE_NAME", "refuelings"),
        commits_table=os.getenv("COMMITS_TABLE_NAME", "commits"),
    )
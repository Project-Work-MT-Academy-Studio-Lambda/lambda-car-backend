from dataclasses import dataclass
import os


@dataclass(frozen=True)
class DynamoDbConfig:
    region_name: str
    users_table: str
    trips_table: str
    cars_table: str
    refuelings_table: str
    commits_table: str


def load_dynamodb_config() -> DynamoDbConfig:
    return DynamoDbConfig(
        region_name=os.getenv("AWS_REGION", "eu-west-1"),
        users_table=os.getenv("USERS_TABLE", "users"),
        trips_table=os.getenv("TRIPS_TABLE", "trips"),
        cars_table=os.getenv("CARS_TABLE", "cars"),
        refuelings_table=os.getenv("REFUELINGS_TABLE", "refuelings"),
        commits_table=os.getenv("COMMITS_TABLE", "commits"),
    )
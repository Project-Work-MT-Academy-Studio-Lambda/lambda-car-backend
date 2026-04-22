from infrastructure.dynamodb.client import create_dynamodb_resource
from infrastructure.dynamodb.config import load_dynamodb_config


class DynamoDbTables:
    def __init__(self):
        resource = create_dynamodb_resource()
        config = load_dynamodb_config()

        self.users = resource.Table(config.users_table)
        self.trips = resource.Table(config.trips_table)
        self.cars = resource.Table(config.cars_table)
        self.refuelings = resource.Table(config.refuelings_table)
        self.commits = resource.Table(config.commits_table)
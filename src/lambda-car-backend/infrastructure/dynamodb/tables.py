from infrastructure.dynamodb.client import create_dynamodb_resource
from infrastructure.dynamodb.config import load_dynamodb_config


class DynamoDbTables:
    def __init__(self):
        resource = create_dynamodb_resource()
        config = load_dynamodb_config()

        self.user_table = resource.Table(config.users_table)
        self.trip_table = resource.Table(config.trips_table)
        self.car_table = resource.Table(config.cars_table)
        self.refueling_table = resource.Table(config.refuelings_table)
        self.commit_table = resource.Table(config.commits_table)
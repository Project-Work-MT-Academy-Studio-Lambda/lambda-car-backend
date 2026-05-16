from .client import create_dynamodb_resource
from .config import load_dynamodb_config


class DynamoDbTables:
    def __init__(self):
        self.resource = create_dynamodb_resource()
        config = load_dynamodb_config()

        self.table_names = {
            "users": config.users_table,
            "trips": config.trips_table,
            "cars": config.cars_table,
            "refuelings": config.refuelings_table,
            "commits": config.commits_table,
            "maintenances": config.maintenances_table,
        }

        self.user_table = self.resource.Table(config.users_table)
        self.trip_table = self.resource.Table(config.trips_table)
        self.car_table = self.resource.Table(config.cars_table)
        self.refueling_table = self.resource.Table(config.refuelings_table)
        self.commit_table = self.resource.Table(config.commits_table)
        self.maintenance_table = self.resource.Table(config.maintenances_table)

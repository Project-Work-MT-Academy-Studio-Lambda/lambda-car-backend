from uuid import UUID
from decimal import Decimal
from enum import Enum

from boto3.dynamodb.types import TypeSerializer
from botocore.exceptions import ClientError

from ...domain.car import Car
from ...domain.commit import Commit
from ...domain.errors import ConflictError
from ...domain.maintenance import Maintenance
from ...domain.trip import Trip
from ...repositories.application_transaction import ApplicationTransaction
from ...repositories.application_transaction import ApplicationTransactionManager
from ...constants import Constants
from .mappers.car_mapper import car_to_item
from .mappers.commit_mapper import commit_to_item
from .mappers.maintenance_mapper import maintenance_to_item
from .mappers.trip_mapper import trip_to_item


class DynamoDbApplicationTransaction(ApplicationTransaction):
    def __init__(self, client, table_names: dict[str, str]):
        self.client = client
        self.table_names = table_names
        self.serializer = TypeSerializer()
        self._items: list[dict] = []

    def _normalize_value(self, value):
        if isinstance(value, float):
            return Decimal(str(value))
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, dict):
            return {key: self._normalize_value(inner_value) for key, inner_value in value.items()}
        if isinstance(value, list):
            return [self._normalize_value(inner_value) for inner_value in value]
        return value

    def _put(self, table_key: str, item: dict) -> None:
        normalized_item = self._normalize_value(item)
        self._items.append(
            {
                "Put": {
                    "TableName": self.table_names[table_key],
                    "Item": {key: self.serializer.serialize(value) for key, value in normalized_item.items()},
                }
            }
        )

    def _delete(self, table_key: str, item_id: UUID) -> None:
        self._items.append(
            {
                "Delete": {
                    "TableName": self.table_names[table_key],
                    "Key": {"id": self.serializer.serialize(str(item_id))},
                }
            }
        )

    def save_car(self, car: Car) -> None:
        self._put("cars", car_to_item(car))

    def save_commit(self, commit: Commit) -> None:
        self._put("commits", commit_to_item(commit))

    def save_trip(self, trip: Trip) -> None:
        self._put("trips", trip_to_item(trip))

    def save_maintenance(self, maintenance: Maintenance) -> None:
        self._put("maintenances", maintenance_to_item(maintenance))

    def delete_trip(self, trip_id: UUID) -> None:
        self._delete("trips", trip_id)

    def commit(self) -> None:
        if not self._items:
            return
        try:
            self.client.transact_write_items(TransactItems=self._items)
        except ClientError as exc:
            raise ConflictError(Constants.TRANSACTION_FAILED) from exc


class DynamoDbApplicationTransactionManager(ApplicationTransactionManager):
    def __init__(self, resource, table_names: dict[str, str]):
        self.resource = resource
        self.table_names = table_names

    def begin(self) -> DynamoDbApplicationTransaction:
        return DynamoDbApplicationTransaction(self.resource.meta.client, self.table_names)

from uuid import UUID
from boto3.dynamodb.conditions import Key

from domain.refueling import Refueling
from repositories.refueling_repository import RefuelingRepository
from infrastructure.dynamodb.mappers.refueling_mapper import (
    refueling_to_item,
    item_to_refueling,
)


class DynamoDbRefuelingRepository(RefuelingRepository):
    def __init__(self, refueling_table):
        self.refueling_table = refueling_table

    def get_by_id(self, refueling_id: UUID) -> Refueling | None:
        response = self.refueling_table.get_item(Key={"id": str(refueling_id)})
        item = response.get("Item")
        if item is None:
            return None
        return item_to_refueling(item)

    def save(self, refueling: Refueling) -> None:
        self.refueling_table.put_item(Item=refueling_to_item(refueling))

    def delete(self, refueling_id: UUID) -> None:
        self.refueling_table.delete_item(Key={"id": str(refueling_id)})

    def list_by_car_id(self, car_id: UUID) -> list[Refueling]:
        response = self.refueling_table.query(
            IndexName="car_id-index",
            KeyConditionExpression=Key("car_id").eq(str(car_id)),
        )
        return [item_to_refueling(item) for item in response.get("Items", [])]
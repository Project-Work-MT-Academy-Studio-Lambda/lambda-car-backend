from uuid import UUID
from boto3.dynamodb.conditions import Key, Attr

from ....domain.refueling import Refueling
from ....repositories.refueling_repository import RefuelingRepository
from ..mappers.refueling_mapper import (
    refueling_to_item,
    item_to_refueling,
)

from ....domain.enum.role import Role

class DynamoDbRefuelingRepository(RefuelingRepository):
    def __init__(self, refueling_table):
        self.refueling_table = refueling_table

    def get_by_id(self, refueling_id: UUID, user_id: UUID, user_role: str) -> Refueling | None:
        response = self.refueling_table.get_item(Key={"id": str(refueling_id)})
        item = response.get("Item")
        if item is None:
            return None
        if user_role != Role.ADMIN.value or item["user_id"] != str(user_id):
            return None
        return item_to_refueling(item)

    def save(self, refueling: Refueling) -> None:
        self.refueling_table.put_item(Item=refueling_to_item(refueling))

    def delete(self, refueling_id: UUID) -> None:
        self.refueling_table.delete_item(Key={"id": str(refueling_id)})

    def list_by_car_id(self, car_id: UUID, user_id: UUID, user_role: str) -> list[Refueling]:
        query_params = {
        "IndexName": "car_id-index",
        "KeyConditionExpression": Key("car_id").eq(str(car_id)),
        }
        if not user_role == Role.ADMIN.value:
            query_params["FilterExpression"] = Attr("user_id").eq(str(user_id))
        response = self.refueling_table.query(**query_params)
        return [item_to_refueling(item) for item in response.get("Items", [])]
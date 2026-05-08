from uuid import UUID
from boto3.dynamodb.conditions import Key, Attr

from ....domain.refueling import Refueling
from ....repositories.refueling_repository import RefuelingRepository
from ..mappers.refueling_mapper import (
    refueling_to_item,
    item_to_refueling,
)

from ....domain.enum.role import Role

from ....logger import get_logger

class DynamoDbRefuelingRepository(RefuelingRepository):
    def __init__(self, refueling_table):
        self.refueling_table = refueling_table
        self.logger = get_logger(__name__)

    def get_by_id(self, refueling_id: UUID, user_id: UUID, user_role: str) -> Refueling | None:
        response = self.refueling_table.get_item(Key={"id": str(refueling_id)})
        self.logger.debug(f"Response: {response}")
        item = response.get("Item")
        self.logger.debug(f"Retrieved refueling item from DynamoDB: {item}")
        self.logger.debug(f"User role: {user_role}, User ID: {user_id}, Refueling user ID: {item.get('id') if item else 'N/A'}")
        if item is None:
            return None
        self.logger.debug(f"Checking access for refueling {refueling_id} by user {user_id} with role {user_role}")
        self.logger.debug(f"User role is admin: {user_role == Role.ADMIN.value}")
        if user_role != Role.ADMIN.value and item["id"] != str(user_id):
            self.logger.warning(f"Access denied for refueling {refueling_id} by user {user_id}")
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
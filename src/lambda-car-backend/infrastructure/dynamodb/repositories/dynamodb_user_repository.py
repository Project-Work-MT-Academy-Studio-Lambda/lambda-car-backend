from uuid import UUID
from boto3.dynamodb.conditions import Key

from domain.user import User
from repositories.user_repository import UserRepository
from infrastructure.dynamodb.mappers.user_mapper import user_to_item, item_to_user


class DynamoDbUserRepository(UserRepository):
    def __init__(self, user_table):
        self.user_table = user_table

    def get_by_id(self, user_id: UUID) -> User | None:
        response = self.user_table.get_item(Key={"id": str(user_id)})
        item = response.get("Item")
        if item is None:
            return None
        return item_to_user(item)

    def get_by_email(self, email: str) -> User | None:
        response = self.user_table.query(
            IndexName="email-index",
            KeyConditionExpression=Key("email").eq(email),
        )
        items = response.get("Items", [])
        if not items:
            return None
        return item_to_user(items[0])

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def save(self, user: User) -> None:
        self.user_table.put_item(Item=user_to_item(user))

    def delete(self, user_id: UUID) -> None:
        self.user_table.delete_item(Key={"id": str(user_id)})
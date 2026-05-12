from uuid import UUID
from boto3.dynamodb.conditions import Key

from ....domain.user import User
from ....repositories.user_repository import UserRepository
from ..mappers.user_mapper import user_to_item, item_to_user
from ....logger import get_logger


class DynamoDbUserRepository(UserRepository):
    def __init__(self, user_table):
        self.user_table = user_table
        self.logger = get_logger(__name__)

    def get_by_id(self, user_id: UUID) -> User | None:
        response = self.user_table.get_item(Key={"id": str(user_id)})
        item = response.get("Item")
        if item is None:
            return None
        return item_to_user(item)
    
    def find_all(self) -> list[User]:
        response = self.user_table.scan()
        items = response.get("Items", [])
        return [item_to_user(item) for item in items]

    def get_by_email(self, email: str) -> User | None:
        try:
            self.logger.debug(f"Fetching user by email: {email}")
            response = self.user_table.query(
                IndexName="email-index",
                KeyConditionExpression=Key("email").eq(email),
            )
            self.logger.debug(f"DynamoDB query response: {response}")
            items = response.get("Items", [])
            if not items:
                return None
            self.logger.debug(f"User found for email {email}: {items[0]}")
            return item_to_user(items[0])
        except Exception as e:
            self.logger.error(f"Error fetching user by email {email}: {e}")
            raise

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def save(self, user: User) -> None:
        self.user_table.put_item(Item=user_to_item(user))

    def delete(self, user_id: UUID) -> None:
        self.user_table.delete_item(Key={"id": str(user_id)})
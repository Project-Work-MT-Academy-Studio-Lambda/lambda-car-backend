from uuid import UUID
from boto3.dynamodb.conditions import Key, Attr

from ....domain.commit import Commit
from ....repositories.commit_repository import CommitRepository
from ..mappers.commit_mapper import commit_to_item, item_to_commit

from ....domain.enum.role import Role


class DynamoDbCommitRepository(CommitRepository):
    def __init__(self, commit_table):
        self.commit_table = commit_table

    def get_by_id(self, commit_id: UUID) -> Commit | None:
        response = self.commit_table.get_item(Key={"id": str(commit_id)})
        item = response.get("Item")
        if item is None:
            return None
        return item_to_commit(item)

    def get_by_code(self, code: str) -> Commit | None:
        response = self.commit_table.query(
            IndexName="code-index",
            KeyConditionExpression=Key("code").eq(code),
        )
        items = response.get("Items", [])
        if not items:
            return None
        return item_to_commit(items[0])
    
    def get_by_trip_id(self, trip_id: UUID, user_id: UUID, user_role: str) -> list[Commit]:
        query_params = {
        "IndexName": "trip_id-index",
        "KeyConditionExpression": Key("trip_id").eq(str(trip_id)),
        }
        if not user_role == Role.ADMIN.value:
            query_params["FilterExpression"] = Attr("user_id").eq(str(user_id))
        response = self.commit_table.query(**query_params)
        return [item_to_commit(item) for item in response.get("Items", [])]
    
    def find_all(self) -> list[Commit]:
        response = self.commit_table.scan()
        return [item_to_commit(item) for item in response.get("Items", [])]
    
    def find_by_status(self, status):
        response = self.commit_table.scan(
            FilterExpression=Attr("status").eq(status)
        )
        return [item_to_commit(item) for item in response.get("Items", [])]
    
    def find_by_trip_id(self, trip_id: UUID) -> list[Commit]:
        response = self.commit_table.query(
            IndexName="trip_id-index",
            KeyConditionExpression=Key("trip_id").eq(str(trip_id)),
        )
        return [item_to_commit(item) for item in response.get("Items", [])]

    def save(self, commit: Commit) -> None:
        self.commit_table.put_item(Item=commit_to_item(commit))

    def delete(self, commit_id: UUID) -> None:
        self.commit_table.delete_item(Key={"id": str(commit_id)})
    
    def close_commit_by_trip_id(self, trip_id: UUID):
        commits = self.find_by_trip_id(trip_id)
        for commit in commits:
            commit.status = "closed"
            self.save(commit)
from uuid import UUID
from boto3.dynamodb.conditions import Key

from domain.commit import Commit
from repositories.commit_repository import CommitRepository
from infrastructure.dynamodb.mappers.commit_mapper import commit_to_item, item_to_commit


class DynamoDbCommitRepository(CommitRepository):
    def __init__(self, commit_table):
        self.commit_table = commit_table

    def get_by_id(self, commit_id: UUID) -> Commit | None:
        response = self.commit_table.get_item(Key={"id": str(commit_id)})
        item = response.get("Item")
        if item is None:
            return None
        return item_to_commit(item)

    def save(self, commit: Commit) -> None:
        self.commit_table.put_item(Item=commit_to_item(commit))

    def delete(self, commit_id: UUID) -> None:
        self.commit_table.delete_item(Key={"id": str(commit_id)})

    def list_by_trip_id(self, trip_id: UUID) -> list[Commit]:
        response = self.commit_table.query(
            IndexName="trip_id-index",
            KeyConditionExpression=Key("trip_id").eq(str(trip_id)),
        )
        return [item_to_commit(item) for item in response.get("Items", [])]
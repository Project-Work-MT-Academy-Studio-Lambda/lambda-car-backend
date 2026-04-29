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

    def get_by_code(self, code: str) -> Commit | None:
        response = self.commit_table.query(
            IndexName="code-index",
            KeyConditionExpression=Key("code").eq(code),
        )
        items = response.get("Items", [])
        if not items:
            return None
        return item_to_commit(items[0])

    def save(self, commit: Commit) -> None:
        self.commit_table.put_item(Item=commit_to_item(commit))

    def delete(self, commit_id: UUID) -> None:
        self.commit_table.delete_item(Key={"id": str(commit_id)})
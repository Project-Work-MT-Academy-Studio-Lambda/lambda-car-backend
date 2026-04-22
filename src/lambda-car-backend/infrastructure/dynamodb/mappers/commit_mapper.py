from domain.commit import Commit
from uuid import UUID

def commit_to_dynamodb_item(commit: Commit) -> dict:
    return {
        'id': str(commit.id),
        'trip_id': str(commit.trip_id),
        'code': commit.code,
        'description': commit.description
    }

def dynamodb_item_to_commit(item: dict) -> Commit:
    return Commit(
        id=UUID(item['id']),
        trip_id=UUID(item['trip_id']),
        code=item['code'],
        description=item['description']
    )
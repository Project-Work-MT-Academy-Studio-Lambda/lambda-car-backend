# infrastructure/dynamodb/mappers/commit_mapper.py

from uuid import UUID
from domain.commit import Commit


def commit_to_item(commit: Commit) -> dict:
    return {
        "id": str(commit.id),
        "code": commit.code,
        "description": commit.description,
    }


def item_to_commit(item: dict) -> Commit:
    return Commit(
        id=UUID(item["id"]),
        code=item["code"],
        description=item["description"],
    )
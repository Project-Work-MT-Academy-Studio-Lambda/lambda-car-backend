from uuid import UUID
from ....domain.commit import Commit


def commit_to_item(commit: Commit) -> dict:
    return {
        "id": str(commit.id),
        "trip_id": str(commit.trip_id) if commit.trip_id else None,
        "code": commit.code,
        "description": commit.description,
        "status": commit.status,
    }

def item_to_commit(item: dict) -> Commit:
    return Commit(
        id=UUID(item["id"]),
        trip_id=UUID(item["trip_id"]) if item.get("trip_id") else None,
        code=item["code"],
        description=item["description"],
        status=item["status"],
    )
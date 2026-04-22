from dataclasses import dataclass
from uuid import UUID

@dataclass
class CreateCommitCommand:
    trip_id: UUID
    code: str
    description: str

class UpdateCommitCommand:
    commit_id: UUID
    trip_id: UUID
    code: str
    description: str
from dataclasses import dataclass
from uuid import UUID

@dataclass
class Commit:
    id: UUID
    trip_id: UUID
    code: str
    description: str

    def __post_init__(self):
        if not self.code:
            raise ValueError("Code cannot be empty")
        if not self.description:
            raise ValueError("Description cannot be empty")
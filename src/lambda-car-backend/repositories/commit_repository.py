from typing import Protocol
from uuid import UUID
from domain.commit import Commit

class CommitRepository(Protocol):
    def get_by_id(self, commit_id: UUID) -> Commit | None:
        ...

    def save(self, commit: Commit) -> None:
        ...

    def delete(self, commit_id: UUID) -> None:
        ...
    
    def get_by_code(self, code: str) -> Commit | None:
        ...
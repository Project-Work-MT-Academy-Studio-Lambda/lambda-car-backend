from typing import Protocol
from uuid import UUID
from ..domain.commit import Commit

class CommitRepository(Protocol):
    def get_by_id(self, commit_id: UUID) -> Commit | None:
        ...

    def save(self, commit: Commit) -> None:
        ...

    def delete(self, commit_id: UUID) -> None:
        ...
    
    def get_by_code(self, code: str) -> Commit | None:
        ...
    
    def find_by_trip_id(self, trip_id: UUID) -> list[Commit]:
        ...
    
    def find_all(self) -> list[Commit]:
        ...
    
    def find_by_status(self, status: str) -> list[Commit]:
        ...
    
    def close_commit_by_trip_id(self, trip_id: UUID) -> None:
        ...
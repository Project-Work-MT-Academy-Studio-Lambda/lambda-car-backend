from dataclasses import dataclass
from uuid import UUID
from typing import List

@dataclass
class CreateCommitCommand:
    code: str
    description: str

class UpdateCommitCommand:
    commit_id: UUID
    code: str
    description: str

@dataclass(frozen=True)
class ImportCommitItemCommand:
    code: str
    description: str

@dataclass(frozen=True)
class ImportCommitsCommand:
    items: List[ImportCommitItemCommand]
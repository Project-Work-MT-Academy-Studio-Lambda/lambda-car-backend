from dataclasses import dataclass
from uuid import UUID
from ..constants import Constants
from .enum.commit_status import CommitStatus

@dataclass
class Commit:
    id: UUID
    code: str
    description: str
    status: CommitStatus = CommitStatus.BACKLOG
    trip_id: UUID | None = None

    def __post_init__(self):
        if not self.code:
            raise ValueError(Constants.CODE_CANNOT_BE_EMPTY)
        if not self.description:
            raise ValueError(Constants.DESCRIPTION_CANNOT_BE_EMPTY)
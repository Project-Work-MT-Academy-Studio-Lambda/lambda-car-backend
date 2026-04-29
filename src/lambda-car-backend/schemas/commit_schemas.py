from uuid import UUID
from pydantic import BaseModel, Field
from typing import List

from domain.commit import Commit


class CreateCommitRequest(BaseModel):
    code: str
    description: str

class UpdateCommitRequest(BaseModel):
    code: str
    description: str


class CommitResponse(BaseModel):
    id: UUID
    code: str
    description: str

    @classmethod
    def from_domain(cls, commit: Commit) -> "CommitResponse":
        return cls(
            id=commit.id,
            code=commit.code,
            description=commit.description,
        )

class ImportCommitItemRequest(BaseModel):
    code: str
    description: str


class ImportCommitsRequest(BaseModel):
    items: List[ImportCommitItemRequest]

class ImportCommitsResponse(BaseModel):
    created: int
    updated: int
    skipped: int
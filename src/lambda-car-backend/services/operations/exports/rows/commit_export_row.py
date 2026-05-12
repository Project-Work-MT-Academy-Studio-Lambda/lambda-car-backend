from dataclasses import dataclass

@dataclass(frozen=True)
class CommitExportRow:
    code: str
    description: str
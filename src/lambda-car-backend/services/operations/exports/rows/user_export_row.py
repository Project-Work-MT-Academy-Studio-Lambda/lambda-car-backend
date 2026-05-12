from dataclasses import dataclass

@dataclass(frozen=True)
class UserExportRow:
    name: str
    email: str
    role: str
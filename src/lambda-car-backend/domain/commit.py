from dataclasses import dataclass
from uuid import UUID
from constants import Constants

@dataclass
class Commit:
    id: UUID
    code: str
    description: str

    def __post_init__(self):
        if not self.code:
            raise ValueError(Constants.CODE_CANNOT_BE_EMPTY)
        if not self.description:
            raise ValueError(Constants.DESCRIPTION_CANNOT_BE_EMPTY)
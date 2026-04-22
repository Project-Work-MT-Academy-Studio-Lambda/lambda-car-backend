from dataclasses import dataclass
from uuid import UUID
from constants import Constants
from enum.role import Role

@dataclass
class User:
    id: UUID
    name: str
    email: str
    password: str
    role: Role

    def __post_init__(self):
        if not self.name:
            raise ValueError(Constants.NAME_CANNOT_BE_EMPTY)
        if not self.email:
            raise ValueError(Constants.EMAIL_CANNOT_BE_EMPTY)
        if not self.password:
            raise ValueError(Constants.PASSWORD_CANNOT_BE_EMPTY)
        if not isinstance(self.role, Role):
            raise ValueError(Constants.INVALID_ROLE)
from dataclasses import dataclass
from uuid import UUID
from constants import Constants
from domain.enum.role import Role

@dataclass
class User:
    id: UUID
    name: str
    email: str
    hashed_password: str
    role: Role

    def __post_init__(self):
        if not self.name:
            raise ValueError(Constants.NAME_CANNOT_BE_EMPTY)
        if not self.email:
            raise ValueError(Constants.EMAIL_CANNOT_BE_EMPTY)
        if not self.hashed_password:
            raise ValueError(Constants.PASSWORD_CANNOT_BE_EMPTY)
        if not isinstance(self.role, Role):
            raise ValueError(Constants.INVALID_ROLE)
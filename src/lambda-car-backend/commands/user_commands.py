from dataclasses import dataclass
from uuid import UUID
from domain.enum.role import Role
from constants import Constants

@dataclass
class CreateUserCommand:
    name: str
    email: str
    password: str
    role:Role = Constants.USER

@dataclass
class UpdateUserCommand:
    user_id: UUID
    name: str
    email: str

@dataclass
class ChangePasswordCommand:
    user_id: UUID
    current_password: str
    new_password: str
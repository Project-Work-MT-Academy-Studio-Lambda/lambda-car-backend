from dataclasses import dataclass
from uuid import UUID

@dataclass
class CreateUserCommand:
    name: str
    email: str
    password: str

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
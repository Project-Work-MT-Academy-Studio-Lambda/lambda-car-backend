from uuid import UUID
from pydantic import BaseModel, EmailStr
from domain.user import User
from domain.enum.role import Role 


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role = Role.USER

class UpdateUserRequest(BaseModel):
    name: str
    email: EmailStr
    role: Role


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: Role

    @classmethod
    def from_domain(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
        )

class ChangePasswordRequest(BaseModel):
    new_password: str
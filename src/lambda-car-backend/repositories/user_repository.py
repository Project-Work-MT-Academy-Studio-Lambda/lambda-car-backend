from typing import Protocol
from uuid import UUID
from ..domain.user import User


class UserRepository(Protocol):
    def get_by_id(self, user_id: UUID) -> User | None:
        ...
    
    def find_all(self) -> list[User]:
        ...

    def get_by_email(self, email: str) -> User | None:
        ...

    def exists_by_email(self, email: str) -> bool:
        ...

    def save(self, user: User) -> None:
        ...

    def delete(self, user_id: UUID) -> None:
        ...
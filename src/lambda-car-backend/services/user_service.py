from uuid import UUID, uuid4
from ..domain.user import User
from ..repositories.user_repository import UserRepository
from ..constants import Constants
from ..security.password_hasher import ArgonPasswordHasher

from ..commands.user_commands import (
    CreateUserCommand,
    UpdateUserCommand,
    ChangePasswordCommand
)

from ..logger import get_logger

class UserService:
    def __init__(self, user_repository: UserRepository, password_hasher: ArgonPasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.logger = get_logger(__name__)
    
    def _get_user_or_raise(self, user_id: UUID) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(Constants.USER_NOT_FOUND)
        return user

    def create_user(self, cmd: CreateUserCommand) -> User:
        if self.user_repository.exists_by_email(cmd.email):
            raise ValueError(Constants.EMAIL_ALREADY_USE)
        user = User(id=uuid4(), name=cmd.name, email=cmd.email, hashed_password=self.password_hasher.hash(cmd.password), role=cmd.role)
        self.user_repository.save(user)
        return user
    
    def find_all(self) -> list[User]:
        return self.user_repository.find_all()
    
    def get_user(self, user_id: UUID) -> User | None:
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repository.get_by_email(email)
    
    def update_user(self, cmd: UpdateUserCommand) -> User:
        user = self._get_user_or_raise(cmd.user_id)
        if user.email != cmd.email and self.user_repository.exists_by_email(cmd.email):
            raise ValueError(Constants.EMAIL_ALREADY_USE)
        user.name = cmd.name
        user.email = cmd.email
        self.user_repository.save(user)
        return user
    
    def change_password(self, cmd: ChangePasswordCommand) -> User:
        self.logger.debug(f"Changing password for user_id: {cmd.user_id}")
        user = self._get_user_or_raise(cmd.user_id)
        self.logger.debug(f"User found for password change: {user.id}")
        user.hashed_password = self.password_hasher.hash(cmd.new_password)
        self.user_repository.save(user)
        self.logger.debug(f"Password changed successfully for user_id: {cmd.user_id}")
        return user

    def delete_user(self, user_id: UUID) -> None:
        self.user_repository.get_by_id(user_id)
        self.user_repository.delete(user_id)
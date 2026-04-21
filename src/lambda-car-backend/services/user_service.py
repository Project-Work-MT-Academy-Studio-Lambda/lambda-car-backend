from uuid import UUID, uuid4
from domain.user import User
from repositories.user_repository import UserRepository
from constants import Constants
from security.password_hasher import ArgonPasswordHasher

class UserService:
    def __init__(self, user_repository: UserRepository, password_hasher: ArgonPasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def create_user(self, name: str, email: str, password: str) -> User:
        if self.user_repository.exists_by_email(email):
            raise ValueError(Constants.EMAIL_ALREADY_USE)
        
        user = User(id=uuid4(), name=name, email=email, hashed_password=self.password_hasher.hash(password))
        self.user_repository.save(user)
        return user
    
    def get_user(self, user_id: UUID) -> User | None:
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.user_repository.get_by_email(email)
    
    def update_user(self, user_id: UUID, name: str, email: str, password: str) -> User:
        user = self.get_user(user_id)
        if not user:
            raise ValueError(Constants.USER_NOT_FOUND)
        if user.email != email and self.user_repository.exists_by_email(email):
            raise ValueError(Constants.EMAIL_ALREADY_USE)
        user.name = name
        user.email = email
        self.user_repository.save(user)
        return user
    
    def change_password(self, user_id: UUID, current_password: str, new_password: str) -> User:
        user = self.get_user(user_id)
        if not user:
            raise ValueError(Constants.USER_NOT_FOUND)
        if not self.password_hasher.verify(current_password, user.hashed_password):
            raise ValueError(Constants.INVALID_CREDENTIALS)
        user.hashed_password = self.password_hasher.hash(new_password)
        self.user_repository.save(user)
        return user

    def delete_user(self, user_id: UUID) -> None:
        self.user_repository.get_by_id(user_id)
        self.user_repository.delete(user_id)
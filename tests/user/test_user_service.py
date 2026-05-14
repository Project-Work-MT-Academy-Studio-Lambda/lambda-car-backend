import pytest

from tests.conftest import USER_ID, app_module


class FakeUserRepository:
    def __init__(self, user=None, email_exists=False):
        self.user = user
        self.email_exists = email_exists
        self.saved = None
        self.deleted_id = None

    def exists_by_email(self, email):
        return self.email_exists

    def save(self, user):
        self.saved = user
        self.user = user

    def find_all(self):
        return [self.user] if self.user else []

    def get_by_id(self, user_id):
        if self.user and self.user.id == user_id:
            return self.user
        return None

    def get_by_email(self, email):
        if self.user and self.user.email == email:
            return self.user
        return None

    def delete(self, user_id):
        self.deleted_id = user_id


class FakePasswordHasher:
    def hash(self, password):
        return f"hashed-{password}"


class TestUserService:
    def test_create_user_hashes_password_and_saves(self):
        service_module = app_module("services.user_service")
        command_module = app_module("commands.user_commands")
        Role = app_module("domain.enum.role").Role
        repository = FakeUserRepository()
        service = service_module.UserService(repository, FakePasswordHasher())

        user = service.create_user(
            command_module.CreateUserCommand(
                name="Mario Rossi",
                email="user@test.com",
                password="secret",
                role=Role.USER,
            )
        )

        assert user.hashed_password == "hashed-secret"
        assert repository.saved == user

    def test_create_user_rejects_duplicate_email(self):
        service_module = app_module("services.user_service")
        command_module = app_module("commands.user_commands")
        Role = app_module("domain.enum.role").Role
        service = service_module.UserService(FakeUserRepository(email_exists=True), FakePasswordHasher())

        with pytest.raises(ValueError, match="Email already in use"):
            service.create_user(command_module.CreateUserCommand("Mario", "user@test.com", "secret", Role.USER))

    def test_find_get_update_change_password_and_delete(self, user_factory):
        service_module = app_module("services.user_service")
        command_module = app_module("commands.user_commands")
        repository = FakeUserRepository(user=user_factory())
        service = service_module.UserService(repository, FakePasswordHasher())

        assert service.find_all() == [repository.user]
        assert service.get_user(USER_ID) == repository.user

        updated = service.update_user(command_module.UpdateUserCommand(USER_ID, "Mario Bianchi", "mario@test.com"))
        assert updated.name == "Mario Bianchi"

        changed = service.change_password(command_module.ChangePasswordCommand(USER_ID, "new-secret"))
        assert changed.hashed_password == "hashed-new-secret"

        service.delete_user(USER_ID)
        assert repository.deleted_id == USER_ID

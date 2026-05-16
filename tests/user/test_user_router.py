from tests.conftest import ADMIN_ID, USER_ID, app_module


class FakeUserService:
    def __init__(self, user):
        self.user = user
        self.created = None
        self.updated = None
        self.password_changed = None
        self.deleted_id = None

    def find_all(self):
        return [self.user]

    def get_user(self, user_id):
        return self.user

    def create_user(self, cmd):
        self.created = cmd
        return self.user

    def update_user(self, cmd):
        self.updated = cmd
        return self.user

    def change_password(self, cmd):
        self.password_changed = cmd
        return self.user

    def delete_user(self, user_id, current_user_id=None):
        self.deleted_id = user_id


class TestUserRouter:
    def _client(self, api_client_factory, service):
        dependencies = app_module("dependencies")
        CurrentUser = app_module("domain.user").CurrentUser
        Role = app_module("domain.enum.role").Role
        return api_client_factory(
            {
                dependencies.require_admin: lambda: CurrentUser(id=ADMIN_ID, role=Role.ADMIN),
                dependencies.get_user_service: lambda: service,
            }
        )

    def test_admin_user_routes(self, api_client_factory, user_factory):
        service = FakeUserService(user_factory())
        client = self._client(api_client_factory, service)

        assert client.get("/api/v1/lambdacar/admin/users/").status_code == 200
        assert client.get(f"/api/v1/lambdacar/admin/users/{USER_ID}").status_code == 200

        create_payload = {
            "name": "Mario Rossi",
            "email": "user@test.com",
            "password": "secret",
            "role": "USER",
        }
        assert client.post("/api/v1/lambdacar/admin/users/", json=create_payload).status_code == 201
        assert service.created.email == "user@test.com"

        update_payload = {"name": "Mario Bianchi", "email": "mario@test.com", "role": "USER"}
        assert client.put(f"/api/v1/lambdacar/admin/users/{USER_ID}", json=update_payload).status_code == 200
        assert service.updated.user_id == USER_ID

        assert client.put(f"/api/v1/lambdacar/admin/users/{USER_ID}/password", json={"new_password": "new"}).status_code == 204
        assert service.password_changed.user_id == USER_ID

        assert client.delete(f"/api/v1/lambdacar/admin/users/{USER_ID}").status_code == 204
        assert service.deleted_id == USER_ID

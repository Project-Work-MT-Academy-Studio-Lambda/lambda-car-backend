from tests.conftest import ADMIN_ID, COMMIT_ID, app_module


class FakeCommitService:
    def __init__(self, commit):
        self.commit = commit
        self.created = None
        self.updated = None
        self.deleted_id = None

    def find_all_commits(self):
        return [self.commit]

    def find_backlog_commits(self):
        return [self.commit]

    def get_commit(self, commit_id):
        return self.commit

    def create_commit(self, cmd):
        self.created = cmd
        return self.commit

    def update_commit(self, cmd):
        self.updated = cmd
        return self.commit

    def delete_commit(self, commit_id):
        self.deleted_id = commit_id


class TestCommitRouter:
    def _client(self, api_client_factory, service):
        dependencies = app_module("dependencies")
        CurrentUser = app_module("domain.user").CurrentUser
        Role = app_module("domain.enum.role").Role
        return api_client_factory(
            {
                dependencies.require_admin: lambda: CurrentUser(id=ADMIN_ID, role=Role.ADMIN),
                dependencies.get_commit_service: lambda: service,
            }
        )

    def test_admin_commit_crud_routes(self, api_client_factory, commit_factory):
        service = FakeCommitService(commit_factory())
        client = self._client(api_client_factory, service)

        assert client.get("/api/v1/lambdacar/admin/commits/").status_code == 200
        assert client.get("/api/v1/lambdacar/admin/commits/backlog").status_code == 200
        assert client.get(f"/api/v1/lambdacar/admin/commits/{COMMIT_ID}").status_code == 200

        create_payload = {"code": "COMM-001", "description": "Intervento cliente Napoli"}
        assert client.post("/api/v1/lambdacar/admin/commits/", json=create_payload).status_code == 201
        assert service.created.code == "COMM-001"

        update_payload = {**create_payload, "status": "BACKLOG"}
        assert client.put(f"/api/v1/lambdacar/admin/commits/{COMMIT_ID}", json=update_payload).status_code == 200
        assert service.updated.commit_id == COMMIT_ID

        assert client.delete(f"/api/v1/lambdacar/admin/commits/{COMMIT_ID}").status_code == 204
        assert service.deleted_id == COMMIT_ID

import pytest

from tests.conftest import COMMIT_ID, TRIP_ID, app_module


class FakeCommitRepository:
    def __init__(self, commit=None):
        self.commit = commit
        self.saved = None
        self.deleted_id = None

    def get_by_id(self, commit_id):
        if self.commit and self.commit.id == commit_id:
            return self.commit
        return None

    def save(self, commit):
        self.saved = commit
        self.commit = commit

    def delete(self, commit_id):
        self.deleted_id = commit_id

    def find_all(self):
        return [self.commit] if self.commit else []

    def find_by_status(self, status):
        return [self.commit] if self.commit and self.commit.status == status else []

    def find_by_trip_id(self, trip_id):
        return [self.commit] if self.commit and self.commit.trip_id == trip_id else []

    def get_by_code(self, code):
        if self.commit and self.commit.code == code:
            return self.commit
        return None


class FakeTripRepository:
    def __init__(self, trip=None):
        self.trip = trip

    def get_by_id(self, trip_id):
        if self.trip and self.trip.id == trip_id:
            return self.trip
        return None


class TestCommitService:
    def test_create_get_update_delete_and_list(self, commit_factory):
        service_module = app_module("services.commit_service")
        command_module = app_module("commands.commit_commands")
        repository = FakeCommitRepository()
        service = service_module.CommitService(repository, FakeTripRepository())

        created = service.create_commit(command_module.CreateCommitCommand(code="COMM-001", description="Task"))
        assert created.code == "COMM-001"
        assert repository.saved == created

        updated = service.update_commit(
            command_module.UpdateCommitCommand(commit_id=created.id, code="COMM-002", description="Task aggiornata")
        )
        assert updated.code == "COMM-002"
        assert service.find_all_commits() == [updated]

        service.delete_commit(updated.id)
        assert repository.deleted_id == updated.id

    def test_get_commit_raises_when_missing(self):
        service_module = app_module("services.commit_service")
        service = service_module.CommitService(FakeCommitRepository(), FakeTripRepository())

        with pytest.raises(ValueError, match="Commit not found"):
            service.get_commit(COMMIT_ID)

    def test_get_commits_for_trip_validates_trip(self, commit_factory, trip_factory):
        service_module = app_module("services.commit_service")
        commit = commit_factory(trip_id=TRIP_ID)
        service = service_module.CommitService(
            FakeCommitRepository(commit=commit),
            FakeTripRepository(trip=trip_factory()),
        )

        assert service.get_commits_for_trip(TRIP_ID) == [commit]

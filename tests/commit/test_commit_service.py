import pytest

from tests.conftest import COMMIT_ID, TRIP_ID, app_module


class FakeCommitRepository:
    def __init__(self, commit=None, commits=None):
        self.commit = commit
        self.commits = commits
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
        if self.commits is not None:
            return self.commits
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

    def test_import_commits_creates_backlog_commits(self):
        service_module = app_module("services.commit_service")
        command_module = app_module("commands.commit_commands")
        CommitStatus = app_module("domain.enum.commit_status").CommitStatus
        repository = FakeCommitRepository()
        service = service_module.CommitService(repository, FakeTripRepository())

        result = service.import_commits(
            command_module.ImportCommitsCommand(
                items=[
                    command_module.ImportCommitItemCommand(
                        code="COMM-010",
                        description="Nuova commessa da Excel",
                    )
                ]
            )
        )

        assert result == {"created": 1, "updated": 0, "skipped": 0}
        assert repository.saved.status == CommitStatus.BACKLOG

    def test_backlog_includes_every_not_done_commit(self, commit_factory):
        service_module = app_module("services.commit_service")
        CommitStatus = app_module("domain.enum.commit_status").CommitStatus
        backlog = commit_factory(code="COMM-010", status=CommitStatus.BACKLOG)
        in_progress = commit_factory(code="COMM-011", status=CommitStatus.IN_PROGRESS)
        done = commit_factory(code="COMM-012", status=CommitStatus.DONE)
        repository = FakeCommitRepository(commits=[backlog, in_progress, done])
        service = service_module.CommitService(repository, FakeTripRepository())

        assert service.find_backlog_commits() == [backlog, in_progress]

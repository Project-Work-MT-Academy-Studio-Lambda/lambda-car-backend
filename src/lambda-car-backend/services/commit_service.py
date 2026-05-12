from uuid import UUID, uuid4

from ..domain.commit import Commit
from ..repositories.commit_repository import CommitRepository
from ..repositories.trip_repository import TripRepository
from ..constants import Constants

from ..commands.commit_commands import (
    CreateCommitCommand,
    UpdateCommitCommand,
    ImportCommitsCommand
)

from ..domain.enum.commit_status import CommitStatus

class CommitService:
    def __init__(
        self,
        commit_repository: CommitRepository,
        trip_repository: TripRepository,
    ):
        self.commit_repository = commit_repository
        self.trip_repository = trip_repository
    
    def _get_commit_or_raise(self, commit_id: UUID) -> Commit:
        commit = self.commit_repository.get_by_id(commit_id)
        if not commit:
            raise ValueError(Constants.COMMIT_NOT_FOUND)
        return commit

    def create_commit(
        self,
        cmd: CreateCommitCommand
    ) -> Commit:

        commit = Commit(
            id=uuid4(),
            code=cmd.code,
            description=cmd.description,
            status=CommitStatus.BACKLOG.value,
        )

        self.commit_repository.save(commit)
        return commit

    def get_commit(self, commit_id: UUID) -> Commit:
        commit = self._get_commit_or_raise(commit_id)
        return commit

    def get_commits_for_trip(self, trip_id: UUID) -> list[Commit]:
        trip = self.trip_repository.get_by_id(trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)

        return self.commit_repository.find_by_trip_id(trip_id)
    
    def find_all_commits(self) -> list[Commit]:
        return self.commit_repository.find_all()
    
    def find_backlog_commits(self) -> list[Commit]:
        return self.commit_repository.find_by_status(CommitStatus.BACKLOG)

    def update_commit(
        self,
        cmd: UpdateCommitCommand
    ) -> Commit:
        commit = self._get_commit_or_raise(cmd.commit_id)
        commit.code = cmd.code
        commit.description = cmd.description

        self.commit_repository.save(commit)
        return commit

    def delete_commit(self, commit_id: UUID) -> None:
        commit = self._get_commit_or_raise(commit_id)
        self.commit_repository.delete(commit_id)

    def import_commits(self, cmd: ImportCommitsCommand) -> dict:
        created = 0
        updated = 0
        skipped = 0

        seen_codes = set()

        for item in cmd.items:
            code = (item.code or "").strip()
            description = (item.description or "").strip()

            if not code or not description:
                skipped += 1
                continue

            if code in seen_codes:
                skipped += 1
                continue

            seen_codes.add(code)

            existing = self.commit_repository.get_by_code(code)

            if existing is None:
                commit = Commit(
                    id=uuid4(),
                    code=code,
                    description=description,
                )
                self.commit_repository.save(commit)
                created += 1
            else:
                if existing.description != description:
                    existing.description = description
                    self.commit_repository.save(existing)
                    updated += 1
                else:
                    skipped += 1

        return {
            "created": created,
            "updated": updated,
            "skipped": skipped,
        }
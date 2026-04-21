from uuid import UUID, uuid4

from domain.commit import Commit
from repositories.commit_repository import CommitRepository
from repositories.trip_repository import TripRepository
from constants import Constants


class CommitService:
    def __init__(
        self,
        commit_repository: CommitRepository,
        trip_repository: TripRepository,
    ):
        self.commit_repository = commit_repository
        self.trip_repository = trip_repository

    def create_commit(
        self,
        trip_id: UUID,
        code: str,
        description: str | None = None,
    ) -> Commit:
        trip = self.trip_repository.get_by_id(trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)

        commit = Commit(
            id=uuid4(),
            trip_id=trip_id,
            code=code,
            description=description,
        )

        self.commit_repository.save(commit)
        return commit

    def get_commit(self, commit_id: UUID) -> Commit:
        commit = self.commit_repository.get_by_id(commit_id)
        if not commit:
            raise ValueError(Constants.COMMIT_NOT_FOUND)
        return commit

    def get_commits_for_trip(self, trip_id: UUID) -> list[Commit]:
        trip = self.trip_repository.get_by_id(trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)

        return self.commit_repository.list_by_trip_id(trip_id)

    def update_commit(
        self,
        commit_id: UUID,
        trip_id: UUID,
        code: str,
        description: str | None = None,
    ) -> Commit:
        commit = self.get_commit(commit_id)

        trip = self.trip_repository.get_by_id(trip_id)
        if not trip:
            raise ValueError(Constants.TRIP_NOT_FOUND)

        commit.trip_id = trip_id
        commit.code = code
        commit.description = description

        self.commit_repository.save(commit)
        return commit

    def delete_commit(self, commit_id: UUID) -> None:
        commit = self.get_commit(commit_id)
        if not commit:
            raise ValueError(Constants.COMMIT_NOT_FOUND)
        self.commit_repository.delete(commit_id)
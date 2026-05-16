from typing import Protocol
from uuid import UUID

from ..domain.car import Car
from ..domain.commit import Commit
from ..domain.maintenance import Maintenance
from ..domain.trip import Trip


class ApplicationTransaction(Protocol):
    def save_car(self, car: Car) -> None:
        ...

    def save_commit(self, commit: Commit) -> None:
        ...

    def save_trip(self, trip: Trip) -> None:
        ...

    def save_maintenance(self, maintenance: Maintenance) -> None:
        ...

    def delete_trip(self, trip_id: UUID) -> None:
        ...

    def commit(self) -> None:
        ...


class ApplicationTransactionManager(Protocol):
    def begin(self) -> ApplicationTransaction:
        ...

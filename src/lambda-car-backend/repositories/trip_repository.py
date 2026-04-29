from typing import Protocol
from uuid import UUID
from domain.trip import Trip

class TripRepository(Protocol):
    def get_by_id(self, trip_id: UUID) -> Trip | None:
        ...

    def save(self, trip: Trip) -> None:
        ...

    def delete(self, trip_id: UUID) -> None:
        ...
    
    def list_by_user_id(self, user_id: UUID) -> list[Trip]:
        ...
    
    def list_by_car_id(self, car_id: UUID) -> list[Trip]:
        ...

    def get_active_trip_by_car_id(self, car_id: UUID) -> Trip | None:
        ...
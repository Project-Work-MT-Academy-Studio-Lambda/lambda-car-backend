from typing import Protocol
from uuid import UUID
from domain.refueling import Refueling

class RefuelingRepository(Protocol):
    def get_by_id(self, refueling_id: UUID) -> Refueling | None:
        ...

    def save(self, refueling: Refueling) -> None:
        ...

    def delete(self, refueling_id: UUID) -> None:
        ...
    
    def list_by_car_id(self, car_id: UUID) -> list[Refueling]:
        ...
        
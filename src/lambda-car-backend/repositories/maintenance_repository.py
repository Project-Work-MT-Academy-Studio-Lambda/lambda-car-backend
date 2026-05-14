from typing import Protocol
from uuid import UUID
from ..domain.maintenance import Maintenance

class MaintenanceRepository(Protocol):
    def get_by_id(self, maintenance_id: UUID) -> Maintenance | None:
        ...

    def save(self, maintenance: Maintenance) -> None:
        ...

    def delete(self, maintenance_id: UUID) -> None:
        ...
    
    def find_by_car_id(self, car_id: UUID) -> list[Maintenance]:
        ...
    
    def find_all(self) -> list[Maintenance]:
        ...
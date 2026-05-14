from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from ..domain.enum.maintenance_type import MaintenanceType

@dataclass(frozen=True)
class CreateMaintenanceCommand:
    car_id: UUID
    description: str
    date: datetime
    km_at_maintenance: int
    cost: float
    type: MaintenanceType

@dataclass(frozen=True)
class UpdateMaintenanceCommand:
    maintenance_id: UUID
    car_id: UUID
    description: str
    date: datetime
    km_at_maintenance: int
    cost: float
    type: MaintenanceType

@dataclass(frozen=True)
class DeleteMaintenanceCommand:
    maintenance_id: UUID

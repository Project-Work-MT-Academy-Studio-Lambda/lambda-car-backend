from pydantic import BaseModel
from datetime import datetime
from ..domain.enum.maintenance_type import MaintenanceType 
from ..domain.maintenance import Maintenance
from uuid import UUID

class CreateMaintenanceRequest(BaseModel):
    car_id: UUID
    date: datetime
    km_at_maintenance: int
    cost: float
    description: str
    type: MaintenanceType

class UpdateMaintenanceRequest(BaseModel):
    car_id: UUID
    date: datetime
    km_at_maintenance: int
    cost: float
    description: str
    type: MaintenanceType

class MaintenanceResponse(BaseModel):
    id: str
    car_id: str
    date: datetime
    km_at_maintenance: int
    cost: float
    description: str
    type: MaintenanceType

    @classmethod
    def from_domain(cls, maintenance: Maintenance) -> "MaintenanceResponse":
        return cls(
            id=str(maintenance.id),
            car_id=str(maintenance.car_id),
            date=maintenance.date,
            km_at_maintenance=maintenance.km_at_maintenance,
            cost=float(maintenance.cost),
            description=maintenance.description,
            type=maintenance.type,
        )
